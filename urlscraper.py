import os

import re

from telethon import TelegramClient

from telethon.tl.types import MessageEntityTextUrl

import pandas as pd

from colorama import Fore, Style

import details as ds



# Login details

api_id = ds.apiID

api_hash = ds.apiHash

phone = ds.number



client = TelegramClient(phone, api_id, api_hash)

client.connect()



if not client.is_user_authorized():

    client.send_code_request(phone)

    client.sign_in(phone, input('Enter the code: '))



print('This tool will scrape a Telegram channel for all channel links (https://t.me/*) within comments.')

print()



while True:

    try:

        channel_name = input("Please enter a Telegram channel name: ")

        print(f'You entered "{channel_name}"')

        answer = input('Is this correct? (y/n) ')

        if answer == 'y':

            print(f'Scraping URLs from {channel_name}...')

            break

    except:

        continue



async def main():

    urls = set()  # Use a set to deduplicate URLs



    async for message in client.iter_messages(channel_name):

        if message.entities is not None:

            for entity in message.entities:

                if isinstance(entity, MessageEntityTextUrl):

                    url = entity.url

                    if 'https://t.me/' in url:

                        match = re.match(r'https?://t\.me/([^/\s]+)/?', url)

                        if match:

                            channel_link = f'https://t.me/{match.group(1)}'

                            urls.add(channel_link)

                            print(f"URL - {Fore.CYAN}https://t.me/{match.group(1)}{Style.RESET_ALL}")

        else:

            if message.text and isinstance(message.text, str):

                regex = r'https?://t\.me/([^/\s]+)/?'

                matches = re.findall(regex, message.text)

                for match in matches:

                    channel_link = f'https://t.me/{match}'

                    urls.add(channel_link)

                    print(f"URL - {Fore.CYAN}https://t.me/{match}{Style.RESET_ALL}")



    urls_folder = 'URLs'

    os.makedirs(urls_folder, exist_ok=True)



    output_filename = os.path.join(urls_folder, f'{channel_name}.csv')



    with open(output_filename, 'w', encoding='utf-8') as file:

        file.write('\n'.join(urls))



    print(f'URLs scraped successfully. Saved to: {output_filename}')



with client:

    client.loop.run_until_complete(main())



again = input('Do you want to scrape more channels? (y/n) ')

if again == 'y':

    print('Restarting...')

    exec(open("urlscraper.py").read())

else:

    pass



launcher = input('Do you want to return to the launcher? (y/n) ')

if launcher == 'y':

    print('Restarting...')

    exec(open("launcher.py").read())

else:

    print('Thank you for using the URL scraper.')

