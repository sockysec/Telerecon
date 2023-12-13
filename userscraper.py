import os
import asyncio
import details as ds
from telethon import TelegramClient, errors
from telethon.tl.types import User
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
    media_directory = os.path.join(user_directory,
                                   f"{sanitized_target_user.lstrip('@')}_media")  # Sub-directory for media
    if not os.path.exists(media_directory):
        os.makedirs(media_directory)

    network_data = []  # To store network interaction data

    async with TelegramClient(phone, api_id, api_hash) as client:
        try:
            entity = await client.get_entity(channel_name)
            target_entity = await client.get_entity(target_user)
            content = []

            post_count = 0  # Initialize post count
            async for post in client.iter_messages(entity, from_user=target_entity):
                text = post.text or ""
                date = post.date
                views = post.views or "N/A"

                try:
                    if isinstance(post.sender, User):
                        username = post.sender.username if post.sender.username else "N/A"
                        first_name = post.sender.first_name if post.sender.first_name else "N/A"
                        last_name = post.sender.last_name if post.sender.last_name else "N/A"
                        user_id = post.sender.id
                    else:
                        # Handle the case where the sender is not a user (e.g., a channel)
                        username = post.sender.username if post.sender.username else "N/A"
                        first_name = "N/A"
                        last_name = "N/A"
                        user_id = post.sender.id
                except Exception as e:
                    username = "N/A"
                    first_name = "N/A"
                    last_name = "N/A"
                    user_id = "N/A"

                message_url = f"https://t.me/{channel_name}/{post.id}"
                channel_name = channel_name.split('/')[-1]  # Extract channel name from the URL

                media = None  # Initialize media as None
                # Check if the message has media (image or voice message) and download_media is True
                if post.media and download_media:
                    media_filename = f'media_{post.id}.jpg'
                    media_path = os.path.join(media_directory, media_filename)
                    await post.download_media(file=media_path)

                content.append(
                    (text, date, username, first_name, last_name, user_id, views, message_url, channel_name, media))

                # Check if the message is a reply to another message
                if post.reply_to_msg_id:
                    replied_to_msg_id = post.reply_to_msg_id
                    original_message = await client.get_messages(entity, ids=replied_to_msg_id)

                    try:
                        # Check if the sender of the original message is a user
                        if isinstance(original_message.sender, User):
                            sender_username = original_message.sender.username if original_message.sender.username else ""
                            sender_first_name = original_message.sender.first_name if original_message.sender.first_name else ""
                            sender_last_name = original_message.sender.last_name if original_message.sender.last_name else ""
                            sender_user_id = original_message.sender.id
                        else:
                            # Handle the case where the sender is not a user
                            sender_username = original_message.sender.username if original_message.sender.username else ""
                            sender_first_name = ""
                            sender_last_name = ""
                            sender_user_id = original_message.sender.id
                    except Exception as e:
                        sender_username = ""
                        sender_first_name = ""
                        sender_last_name = ""
                        sender_user_id = ""
                    
                    receiver_username = username  # Use the sender's username as the receiver's username in a reply
                    receiver_first_name = first_name
                    receiver_last_name = last_name
                    receiver_user_id = user_id

                    interaction_type = "reply"
                    timestamp = post.date

                    network_data.append((sender_username, sender_first_name, sender_last_name, sender_user_id,
                                         receiver_username, receiver_first_name, receiver_last_name, receiver_user_id,
                                         interaction_type, timestamp))

                post_count += 1  # Increment post count
                if post_count % 10 == 0:
                    print(
                        f"{Fore.WHITE}{post_count} Posts scraped in {Fore.LIGHTYELLOW_EX}{channel_name}{Style.RESET_ALL}")

                await asyncio.sleep(REQUEST_DELAY)  # Introduce a delay between requests

            return content, network_data  # Return both content and network data

        except (ValueError, errors.FloodWaitError) as ve:
            print(
                f"{Fore.RED}Error – lacking relevant permissions, or channel is not a chat group{Style.RESET_ALL}")  # Red text for errors
            return [], []  # Return empty lists if there's an error
        except Exception as e:
            print(f"{Fore.RED}Error – {e}{Style.RESET_ALL}")  # Red text for errors
            return [], []  # Return empty lists if there's an error


async def main():
    print()
    target_user = input(f"{Fore.CYAN}Please enter the target user's @username: {Style.RESET_ALL}")
    target_channel = input(f"{Fore.CYAN}Please enter the target channel's @username or invite link: {Style.RESET_ALL}")
    download_media_option = input(
        f"{Fore.CYAN}Would you like to download media from the channel (y/n)? {Style.RESET_ALL}")
    download_media = download_media_option.lower() == 'y'
    print()
    print(f"{Fore.YELLOW}Scraping data can take some time, please be patient.{Style.RESET_ALL}")
    print()

    sanitized_target_user = target_user.replace('@', '').replace('_', '').replace('-', '')

    # Create a directory for the user if it doesn't exist
    user_directory = os.path.join("Collection", sanitized_target_user.lstrip('@'))
    if not os.path.exists(user_directory):
        os.makedirs(user_directory)

    channel_content, network_data = await scrape_user_messages(target_channel, target_user, user_directory,
                                                               download_media, sanitized_target_user)
    message_count = len(channel_content)

    if message_count:
        df = pd.DataFrame(channel_content,
                          columns=['Text', 'Date', 'Username', 'First Name', 'Last Name', 'User ID', 'Views',
                                   'Message URL', 'Channel', 'Media'])
        csv_filename = os.path.join(user_directory, f'{sanitized_target_user}_messages.csv')
        try:
            df.to_csv(csv_filename, index=False)
            print(f'Successfully scraped and saved messages to {csv_filename}.')
        except Exception as e:
            print(f"{Fore.RED}An error occurred while saving to CSV: {e}{Style.RESET_ALL}")  # Red text for errors
    else:
        print(f'No messages found for {target_user} in the specified channel.')

    # Save network interaction data to a CSV file
    network_df = pd.DataFrame(network_data, columns=[
        'Sender_Username', 'Sender_FirstName', 'Sender_LastName', 'Sender_UserID',
        'Receiver_Username', 'Receiver_FirstName', 'Receiver_LastName', 'Receiver_UserID',
        'Interaction_Type', 'Timestamp'
    ])

    network_csv_filename = os.path.join(user_directory, f"{sanitized_target_user.lstrip('@')}_network.csv")
    try:
        network_df.to_csv(network_csv_filename, index=False)
        print(f'Successfully saved network interaction data to {network_csv_filename}.')
    except Exception as e:
        print(f"{Fore.RED}An error occurred while saving network data to CSV: {e}{Style.RESET_ALL}")

    # Ask if the user wants to return to launcher
    launcher = input('Do you want to return to the launcher? (y/n)')

    if launcher == 'y':
        print('Restarting...')
        exec(open("launcher.py").read())


if __name__ == '__main__':
    asyncio.run(main())
