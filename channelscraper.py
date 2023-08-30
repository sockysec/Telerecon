import os
import asyncio
import details as ds
from telethon import TelegramClient, types
import pandas as pd
from tqdm import tqdm
import time

# API details
api_id = ds.apiID
api_hash = ds.apiHash
phone = ds.number

# Rate limiting settings
REQUEST_DELAY = 1  # Delay in seconds between requests

# Function to scrape all posts and messages from a channel
async def scrape_channel_content(channel_name):
    async with TelegramClient(phone, api_id, api_hash) as client:
        try:
            entity = await client.get_entity(channel_name)
            content = []

            async for post in client.iter_messages(entity):
                pbar.set_description(f"Scraping: {post.date}")
                text = post.text or ""
                date = post.date
                sender = post.sender

                if sender:
                    if isinstance(sender, types.User):
                        username = sender.username if sender.username else "N/A"
                        first_name = sender.first_name if sender.first_name else "N/A"
                        last_name = sender.last_name if sender.last_name else "N/A"
                        user_id = sender.id
                    else:
                        username = "N/A"
                        first_name = "N/A"
                        last_name = "N/A"
                        user_id = "N/A"
                else:
                    username = "N/A"
                    first_name = "N/A"
                    last_name = "N/A"
                    user_id = "N/A"

                views = post.views or "N/A"
                message_url = f"https://t.me/{channel_name}/{post.id}"

                content.append((text, date, username, first_name, last_name, user_id, views, message_url))

                await asyncio.sleep(REQUEST_DELAY)  # Introduce a delay between requests

            return content

        except Exception as e:
            print(f"An error occurred: {e}")
            return []

# Main function
async def main():
    while True:
        try:
            channel_name = input("Please enter a Telegram channel name:\n")
            print(f'You entered "{channel_name}"')
            answer = input('Is this correct? (y/n)')
            if answer == 'y':
                print(f'Scraping content from {channel_name}...')
                break
        except:
            continue

    global pbar
    pbar = tqdm(total=100, desc="Scraping Progress")

    content = await scrape_channel_content(channel_name)

    pbar.close()

    if content:
        df = pd.DataFrame(content, columns=['Text', 'Date', 'Username', 'First Name', 'Last Name', 'User ID', 'Views', 'Message URL'])
        csv_filename = f'{channel_name}_content.csv'
        try:
            df.to_csv(csv_filename, index=False)
            print(f'Successfully scraped and saved content to {csv_filename}.')
        except Exception as e:
            print(f"An error occurred while saving to CSV: {e}")
    else:
        print('No content scraped.')

# Asynchronous execution
if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
