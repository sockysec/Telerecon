import os
import asyncio
import details as ds
from telethon.sync import TelegramClient, types
import pandas as pd
from colorama import Fore, Style

api_id = ds.apiID
api_hash = ds.apiHash
phone = ds.number


async def scrape_channel_content(channel_name):
    async with TelegramClient(phone, api_id, api_hash) as client:
        try:
            entity = await client.get_entity(channel_name)
            content = []
            post_count = 0

            async for post in client.iter_messages(entity):
                post_count += 1

                text = post.text or ""
                if sender := post.sender:
                    if isinstance(sender, types.User):
                        username = sender.username or "N/A"
                        first_name = sender.first_name or "N/A"
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

                content.append((text, username, first_name, last_name, user_id, views, message_url))

                if post_count % 10 == 0:
                    print(
                        f"{Fore.WHITE}{post_count} Posts scraped in {Fore.LIGHTYELLOW_EX}{channel_name}{Style.RESET_ALL}")

            return content

        except Exception as e:
            print(f"An error occurred: {Fore.RED}{e}{Style.RESET_ALL}")
            return []


async def main():
    try:
        channel_name = input(
            f"{Fore.CYAN}Please enter a target Telegram channel (e.g., https://t.me/{Fore.LIGHTYELLOW_EX}your_channel{Style.RESET_ALL}):\n")
        print(f'You entered "{Fore.LIGHTYELLOW_EX}{channel_name}{Style.RESET_ALL}"')
        answer = input('Is this correct? (y/n)')
        if answer != 'y':
            return

        output_directory = f"Collection/{channel_name}"
        if not os.path.exists(output_directory):
            os.makedirs(output_directory)

        csv_filename = f'{output_directory}/{channel_name}_messages.csv'
        print(f'Scraping content from {Fore.LIGHTYELLOW_EX}{channel_name}{Style.RESET_ALL}...')

        content = await scrape_channel_content(channel_name)

        if content:
            df = pd.DataFrame(content, columns=['Text', 'Username', 'First Name', 'Last Name', 'User ID', 'Views',
                                                'Message URL'])
            try:
                df.to_csv(csv_filename, index=False)
                print(
                    f'Successfully scraped and saved content to {Fore.LIGHTYELLOW_EX}{csv_filename}{Style.RESET_ALL}.')
            except Exception as e:
                print(f"An error occurred while saving to CSV: {Fore.RED}{e}{Style.RESET_ALL}")
        else:
            print(f'{Fore.RED}No content scraped.{Style.RESET_ALL}')

    except Exception as e:
        print(f"An error occurred: {Fore.RED}{e}{Style.RESET_ALL}")


if __name__ == '__main__':
    asyncio.run(main())
