import os
import asyncio
import details as ds
from telethon import TelegramClient, errors
import pandas as pd
from tqdm import tqdm
from colorama import Fore, Style

# API details
api_id = ds.apiID
api_hash = ds.apiHash
phone = ds.number

# Rate limiting settings
REQUEST_DELAY = 2  # Delay in seconds between requests

async def count_user_posts(channel_name, target_user):
    async with TelegramClient(phone, api_id, api_hash) as client:
        try:
            entity = await client.get_entity(channel_name)
            target_entity = await client.get_entity(target_user)
            post_count = 0

            async for post in client.iter_messages(entity, from_user=target_entity):
                post_count += 1

            return post_count

        except (ValueError, errors.FloodWaitError) as ve:
            print(f"\n{Fore.RED}Error: {ve}{Style.RESET_ALL}")
            return 0
        except Exception as e:
            print(f"\n{Fore.RED}An error occurred: {e}{Style.RESET_ALL}")
            return 0

async def main():
    target_user = input(f"{Fore.CYAN}Please enter the target user's @username or User ID: {Style.RESET_ALL}")
    target_list_filename = input(f"{Fore.CYAN}Please enter the filename of the target channel list (csv/txt): {Style.RESET_ALL}")

    if not os.path.exists(target_list_filename):
        print(f"\n{Fore.RED}Error: The file '{target_list_filename}' does not exist.{Style.RESET_ALL}")
        return

    target_channels = []
    with open(target_list_filename, 'r') as file:
        target_channels = [line.strip() for line in file]

    if not target_channels:
        print(f"\n{Fore.YELLOW}Warning: No target channels found in the input file.{Style.RESET_ALL}")
        return

    post_counts = {}

    for target_channel in target_channels:
        print(f"\n{Fore.CYAN}Checking activity in {Fore.YELLOW}{target_channel}...{Style.RESET_ALL}")
        post_count = await count_user_posts(target_channel, target_user)
        post_counts[target_channel] = post_count

        if post_count > 0:
            print(f"\n{Fore.CYAN}{target_user} has {Fore.GREEN}{post_count}{Fore.CYAN} posts in {Fore.YELLOW}{target_channel}.{Style.RESET_ALL}")
        else:
            print(f"\n{Fore.CYAN}{target_user} has {Fore.RED}no posts{Fore.CYAN} in {Fore.YELLOW}{target_channel}.{Style.RESET_ALL}")

    csv_filename = f'{target_user}_post_counts.csv'
    df = pd.DataFrame(post_counts.items(), columns=['Channel', 'Post Count'])
    df.to_csv(csv_filename, index=False)
    print(f"\n{Fore.GREEN}Success: Post counts saved to {Fore.YELLOW}{csv_filename}{Style.RESET_ALL}")

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
