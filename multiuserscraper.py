import os
import asyncio
import details as ds
from telethon import TelegramClient, errors
import pandas as pd
from colorama import Fore, Style

# API details
api_id = ds.apiID
api_hash = ds.apiHash
phone = ds.number

# Create a directory for saving CSV files and media if it doesn't exist
if not os.path.exists("Collection"):
    os.makedirs("Collection")

# Define the REQUEST_DELAY
REQUEST_DELAY = 1  # Delay in seconds between requests

async def scrape_user_messages(channel_name, target_user, user_directory, download_media, sanitized_target_user):
    media_directory = os.path.join(user_directory, f"{sanitized_target_user.lstrip('@')}_media")  # Sub-directory for media
    if not os.path.exists(media_directory):
        os.makedirs(media_directory)

    async with TelegramClient(phone, api_id, api_hash) as client:
        try:
            entity = await client.get_entity(channel_name)
            target_entity = await client.get_entity(target_user)
            content = []

            post_count = 0  # Initialize post count
            async for post in client.iter_messages(entity, from_user=target_entity):
                text = post.text or ""
                date = post.date
                sender = post.sender
                views = post.views or "N/A"

                username = sender.username if sender.username else "N/A"
                first_name = sender.first_name if sender.first_name else "N/A"
                last_name = sender.last_name if sender.last_name else "N/A"
                user_id = sender.id if sender else "N/A"

                message_url = f"https://t.me/{channel_name}/{post.id}"
                channel_name = channel_name.split('/')[-1]  # Extract channel name from the URL

                media = None  # Initialize media as None
                # Check if the message has media (image or voice message) and download_media is True
                if post.media and download_media:
                    media_filename = f'media_{post.id}.jpg'
                    media_path = os.path.join(media_directory, media_filename)
                    await post.download_media(file=media_path)

                content.append((text, date, username, first_name, last_name, user_id, views, message_url, channel_name, media))

                post_count += 1  # Increment post count
                if post_count % 10 == 0:
                    print(f"{Fore.WHITE}{post_count} Posts scraped in {Fore.LIGHTYELLOW_EX}{channel_name}{Style.RESET_ALL}")

                await asyncio.sleep(REQUEST_DELAY)  # Introduce a delay between requests

            return content

        except (ValueError, errors.FloodWaitError) as ve:
            print(f"{Fore.RED}Error – lacking relevant permissions, or channel is not a chat group{Style.RESET_ALL}")  # Red text for errors
            return []
        except Exception as e:
            print(f"{Fore.RED}Error – lacking relevant permissions, or channel is not a chat group{Style.RESET_ALL}")  # Red text for errors
            return []

async def main():
    print()
    target_user = input(f"{Fore.CYAN}Please enter the target user's @username or User ID: {Style.RESET_ALL}")
    target_list_filename = input(f"{Fore.CYAN}Please enter the filename of the target channel list (csv/txt): {Style.RESET_ALL}")
    download_media_option = input(f"{Fore.CYAN}Would you like to download the target's media (y/n)? {Style.RESET_ALL}")
    download_media = download_media_option.lower() == 'y'
    print()
    print(f"{Fore.YELLOW}Scraping data can take some time, please be patient.{Style.RESET_ALL}")
    print()

    target_channels = []
    with open(target_list_filename, 'r') as file:
        target_channels = [line.strip() for line in file]

    if not target_channels:
        print(f"{Fore.RED}No target channels found in the input file. {Style.RESET_ALL}")
        return

    sanitized_target_user = target_user.replace('@', '').replace('_', '').replace('-', '')

    # Create a directory for the user if it doesn't exist
    user_directory = os.path.join("Collection", sanitized_target_user.lstrip('@'))
    if not os.path.exists(user_directory):
        os.makedirs(user_directory)

    all_messages = []  # To store messages from all channels

    for channel_index, target_channel in enumerate(target_channels, start=1):
        print(f"{Fore.CYAN}Scraping messages from {Fore.LIGHTYELLOW_EX}{target_channel}...{Style.RESET_ALL}")
        channel_content = await scrape_user_messages(target_channel, target_user, user_directory, download_media, sanitized_target_user)
        message_count = len(channel_content)
        print(f"{Fore.LIGHTYELLOW_EX}{message_count}{Style.RESET_ALL} posts collected")
        print()  # Print a blank line between channels

        if message_count:
            all_messages.extend(channel_content)

    if all_messages:
        df = pd.DataFrame(all_messages, columns=['Text', 'Date', 'Username', 'First Name', 'Last Name', 'User ID', 'Views', 'Message URL', 'Channel', 'Media'])
        csv_filename = os.path.join(user_directory, f'{sanitized_target_user}_messages.csv')
        try:
            df.to_csv(csv_filename, index=False)
            print(f'Successfully scraped and saved messages to {csv_filename}.')
        except Exception as e:
            print(f"{Fore.RED}An error occurred while saving to CSV: {e}{Style.RESET_ALL}")  # Red text for errors
    else:
        print(f'No messages found for {target_user} in any of the specified channels.')

    # Ask if the user wants to return to launcher
    launcher = input('Do you want to return to the launcher? (y/n)')

    if launcher == 'y':
        print('Restarting...')
        exec(open("launcher.py").read())

if __name__ == '__main__':
    asyncio.run(main())
