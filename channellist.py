import os

from telethon import TelegramClient

import pandas as pd

from colorama import Fore, Style

import details as ds

import re

from urllib.parse import urlparse





# Login details

api_id = ds.apiID

api_hash = ds.apiHash

phone = ds.number



client = TelegramClient(phone, api_id, api_hash)





async def scrape_forwards(channel_name):

    l = []

    source_urls = []

    count = 0



    async for message in client.iter_messages(channel_name):

        if message.forward is not None:

            try:

                id = message.forward.original_fwd.from_id

                if id is not None:

                    try:

                        ent = await client.get_entity(id)

                        target_channel_entity = await client.get_entity(message.to_id.channel_id)

                        target_channel_title = target_channel_entity.title

                        l.append([ent.title, target_channel_title])

                        source_url = f"https://t.me/{ent.username}"

                        source_urls.append(source_url)

                        count += 1

                        print(f"From {Fore.CYAN + ent.title + Style.RESET_ALL} to {Fore.YELLOW + target_channel_title + Style.RESET_ALL}")

                    except ValueError as e:

                        print("Skipping forward:", str(e))

            except Exception as e:

                print(f"{Fore.RED}Skipping forward: Private/Inaccessible{Style.RESET_ALL}")



    df = pd.DataFrame(l, columns=['From', 'To'])

    source_df = pd.DataFrame(source_urls, columns=['SourceURL'])



    # Create folders if they don't exist

    os.makedirs('Adjacency List', exist_ok=True)

    os.makedirs('Source URLs', exist_ok=True)



    # Remove invalid characters from the channel name

    sanitized_channel_name = re.sub(r'[\/:*?"<>|]', '_', channel_name)



    # Extract the channel name without the prefix

    channel_name_without_prefix = sanitized_channel_name.split('/')[-1]

    if channel_name_without_prefix.startswith('https___t.me_'):

        channel_name_without_prefix = channel_name_without_prefix.replace('https___t.me_', '')



    # Save CSV files in respective folders

    df.to_csv(os.path.join('Adjacency List', f'{channel_name_without_prefix}.csv'), header=False, index=False)

    source_df.to_csv(os.path.join('Source URLs', f'{channel_name_without_prefix}SourceURLs.csv'), header=False, index=False)





async def main():

    channels_file = input("Enter the name of the file containing the list of channels (csv or txt): ")



    # Read the channels from the file and remove duplicates

    with open(channels_file) as file:

        channels = [line.strip() for line in file if line.strip()]

    channels = list(set(channels))



    for channel in channels:

        # Skip invalid Telegram URLs

        parsed_url = urlparse(channel)

        if parsed_url.netloc != 't.me':

            print(f"Skipping invalid Telegram URL: {channel}")

            continue



        print(f"Scraping forwards from {channel}...")

        await scrape_forwards(channel)

        print("CSV files created for", channel)

        print()





with client:

    client.loop.run_until_complete(main())



print('Forwards scraped successfully.')

