import os
import asyncio
import details as ds
from telethon import TelegramClient, types
import pandas as pd
from datetime import datetime, timedelta
from colorama import Fore, Style

api_id = ds.apiID
api_hash = ds.apiHash
phone = ds.number

REQUEST_DELAY = 1

async def scrape_channel_content(channel_name, start_date=None, end_date=None):
    async with TelegramClient(phone, api_id, api_hash) as client:
        try:
            entity = await client.get_entity(channel_name)
            content = []
            post_count = 0

            async for post in client.iter_messages(entity):
                post_count += 1

                date = post.date.replace(tzinfo=None)

                if start_date and date < start_date:
                    continue
                if end_date and date > end_date:
                    break

                text = post.text or ""
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

                if post_count % 10 == 0:
                    print(f"{Fore.WHITE}{post_count} Posts scraped in {Fore.LIGHTYELLOW_EX}{channel_name}{Style.RESET_ALL}")

            return content

        except Exception as e:
            print(f"An error occurred: {Fore.RED}{e}{Style.RESET_ALL}")
            return []

async def main():
    while True:
        try:
            channel_name = input(f"{Fore.CYAN}Please enter a Telegram channel name ({Fore.LIGHTYELLOW_EX}e.g., your_channel{Style.RESET_ALL}):\n")
            print("")
            print(f'You entered "{Fore.LIGHTYELLOW_EX}{channel_name}{Style.RESET_ALL}"')
            answer = input('Is this correct? (y/n)')
            if answer == 'y':
                break
        except:
            continue

    while True:
        try:
            print(f"{Fore.CYAN}Please select a temporal option:{Style.RESET_ALL}")
            print("")
            print("1. Scrape entire channel history")
            print("2. Scrape the last 24 hours")
            print("3. Scrape a custom date range")
            choice = input("Option:")

            if choice == '1':
                start_date = None
                end_date = None
                break
            elif choice == '2':
                end_date = datetime.now()
                start_date = end_date - timedelta(days=1)
                break
            elif choice == '3':
                start_date_str = input("{Fore.CYAN}Enter the start date (YYYY-MM-DD):{Style.RESET_ALL} ")
                end_date_str = input("{Fore.CYAN}Enter the end date (YYYY-MM-DD):{Style.RESET_ALL} ")
                start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
                end_date = datetime.strptime(end_date_str, "%Y-%m-%d")
                break
            else:
                print("")
                print(f"{Fore.RED}Invalid choice. Please select 1, 2, or 3.{Style.RESET_ALL}")
        except:
            continue

    output_directory = f"Collection/{channel_name}"
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    csv_filename = f'{output_directory}/{channel_name}_content.csv'
    print(f'Scraping content from {Fore.LIGHTYELLOW_EX}{channel_name}{Style.RESET_ALL}...')

    content = await scrape_channel_content(channel_name, start_date, end_date)

    if content:
        df = pd.DataFrame(content, columns=['Text', 'Date', 'Username', 'First Name', 'Last Name', 'User ID', 'Views', 'Message URL'])
        try:
            df.to_csv(csv_filename, index=False)
            print(f'Successfully scraped and saved content to {Fore.LIGHTYELLOW_EX}{csv_filename}{Style.RESET_ALL}.')
        except Exception as e:
            print(f"An error occurred while saving to CSV: {Fore.RED}{e}{Style.RESET_ALL}")
    else:
        print(f'{Fore.RED}No content scraped.{Style.RESET_ALL}')

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
