import os
import asyncio
import details as ds
from telethon import TelegramClient, errors, types
import pandas as pd
from colorama import Fore, Style
import subprocess
import sys

# API details
api_id = ds.apiID
api_hash = ds.apiHash
phone = ds.number

# Rate limiting settings
REQUEST_DELAY = 1  # Delay in seconds between requests


async def count_user_posts(client, channel_name, target_user):
    try:
        entity = await client.get_entity(channel_name)
        target_entity = await client.get_entity(target_user)
        post_count = 0

        async for post in client.iter_messages(entity, from_user=target_entity):
            post_count += 1

        return post_count

    except (ValueError, errors.FloodWaitError) as ve:
        print(f"{Fore.RED}Error – lacking relevant permissions, or channel is not a chat group{Style.RESET_ALL}")
        return 0
    except Exception as e:
        print(f"{Fore.RED}Error – lacking relevant permissions, or channel is not a chat group{Style.RESET_ALL}")
        return 0


async def process_target_channels(target_user, target_list_filename):
    if not os.path.exists(target_list_filename):
        print(f"{Fore.RED}Error: The file '{target_list_filename}' does not exist.{Style.RESET_ALL}")
        return

    target_channels = []
    with open(target_list_filename, 'r') as file:
        target_channels = [line.strip() for line in file]

    if not target_channels:
        print(f"{Fore.RED}Warning: No target channels found in the input file.{Style.RESET_ALL}")
        return

    post_counts = {}

    output_directory = os.path.join("Collection", target_user)
    os.makedirs(output_directory, exist_ok=True)  # Create the directory if it doesn't exist

    async with TelegramClient(phone, api_id, api_hash) as client:
        for target_channel in target_channels:
            print()  # Print a blank line between channels
            print(f"{Fore.CYAN}Checking activity in {Fore.YELLOW}{target_channel}...{Style.RESET_ALL}")
            post_count = await count_user_posts(client, target_channel, target_user)
            post_counts[target_channel] = post_count

            if post_count > 0:
                print(
                    f"{Fore.CYAN}{target_user} has {Fore.YELLOW}{post_count}{Fore.CYAN} posts in {Fore.YELLOW}{target_channel}.{Style.RESET_ALL}")
            else:
                print(
                    f"{Fore.CYAN}{target_user} has {Fore.YELLOW}no posts{Fore.CYAN} in {Fore.YELLOW}{target_channel}.{Style.RESET_ALL}")

    csv_filename = os.path.join(output_directory, f'{target_user}_Activity.csv')
    df = pd.DataFrame(post_counts.items(), columns=['Channel', 'Post Count'])
    df.to_csv(csv_filename, index=False)
    print()
    print(f"{Fore.GREEN}Success: Post counts saved to {csv_filename}{Style.RESET_ALL}")


if __name__ == '__main__':
    target_user = input(f"{Fore.CYAN}Please enter the target user's @username or User ID:{Style.RESET_ALL} ")
    target_user = target_user.replace("@", "")  # Remove "@" symbol

    target_list_filename = input(
        f"{Fore.CYAN}Please enter the filename of the target channel list (csv/txt):{Style.RESET_ALL} ")

    asyncio.run(process_target_channels(target_user, target_list_filename))

    # Ask the user if they want to scrape posts
    print()
    scrape_choice = input(
        f"{Fore.CYAN}Do you want to scrape posts from target channels? (y/n): {Style.RESET_ALL} ").strip().lower()

    if scrape_choice == "y":
        # Launch usermultiscraper.py using subprocess and sys.executable
        subprocess.run([sys.executable, "usermultiscraper.py", target_user])
