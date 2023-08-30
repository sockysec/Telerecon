import os
import asyncio
import details as ds
from telethon import TelegramClient, errors, types
import pandas as pd
from tqdm import tqdm

# API details
api_id = ds.apiID
api_hash = ds.apiHash
phone = ds.number

# Rate limiting settings
REQUEST_DELAY = 1  # Delay in seconds between requests

async def scrape_user_messages(channel_name, target_user):
    async with TelegramClient(phone, api_id, api_hash) as client:
        try:
            entity = await client.get_entity(channel_name)
            target_entity = await client.get_entity(target_user)
            content = []

            total_messages = await client.get_messages(entity, limit=0)
            progress_bar = tqdm(total=total_messages, desc="Scraping Progress")

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

                content.append((text, date, username, first_name, last_name, user_id, views, message_url))
                progress_bar.update(1)

                await asyncio.sleep(REQUEST_DELAY)  # Introduce a delay between requests

            progress_bar.close()

            return content

        except (ValueError, errors.FloodWaitError) as ve:
            print(f"Error: {ve}")
            return []
        except Exception as e:
            print(f"An error occurred: {e}")
            return []

async def main():
    while True:
        try:
            channel_name = input("Please enter the target channel name or ID: ")
            target_user = input("Please enter the target user's @username or User ID: ")
            answer = input('Are these inputs correct? (y/n)')
            if answer == 'y':
                break
        except:
            continue
    
    content = await scrape_user_messages(channel_name, target_user)

    if content:
        df = pd.DataFrame(content, columns=['Text', 'Date', 'Username', 'First Name', 'Last Name', 'User ID', 'Views', 'Message URL'])
        csv_filename = f'{target_user}_messages_in_{channel_name}.csv'
        try:
            df.to_csv(csv_filename, index=False)
            print(f'Successfully scraped and saved messages to {csv_filename}.')
        except Exception as e:
            print(f"An error occurred while saving to CSV: {e}")
    else:
        print(f'No messages found for {target_user} in {channel_name}.')

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
