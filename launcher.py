import asyncio

from telethon.sync import TelegramClient

from colorama import init, Fore, Style

# Initialize colorama

init(autoreset=True)


# Function to stop any existing asyncio event loop

def stop_event_loop():
    try:

        loop = asyncio.get_event_loop()

        loop.stop()

    except Exception as e:

        pass


# Launcher code

print(
    f'{Fore.CYAN} __________________________________________________________________'
)

print(
    f'{Fore.CYAN}   _______ ______ _      ______ _____  ______ _____ ____  _   _    '
)

print(Fore.CYAN + r'  |__   __|  ____| |    |  ____|  __ \|  ____/ ____/ __ \| \ | |   ')

print(Fore.CYAN + r'     | |  | |__  | |    | |__  | |__) | |__ | |   | |  | |  \| |   ')

print(
    f'{Fore.CYAN}     | |  |  __| | |    |  __| |  _  /|  __|| |   | |  | | . ` |   '
)

print(Fore.CYAN + r'     | |  | |____| |____| |____| | \ \| |___| |___| |__| | |\  |   ')

print(Fore.CYAN + r'     |_|  |______|______|______|_|  \_\______\_____\____/|_| \_| v2.1')

print(
    f'{Fore.CYAN}___________________________________________________________________'
)

print(Style.RESET_ALL)

print(f'{Fore.YELLOW}                                          ')

print(
    f'{Fore.YELLOW}Welcome to Telerecon, a scraper and reconnaissance framework for Telegram'
)

print("")

print(f'{Fore.YELLOW}Please select an option:')

print(Style.RESET_ALL)

options = {

    'Get user information': 'userdetails.py',

    'Check user activity across a list of channels': 'recon.py',

    'Collect user messages from a target channel': 'userscraper.py',

    'Collect user messages from a list of target channels': 'usermultiscraper.py',

    'Scrape all messages within a channel': 'channelscraper.py',

    'Scrape all t.me URL’s from within a channel': 'urlscraper.py',

    'Scrape forwarding relationships into target channel': 'channels.py',

    'Scrape forwarding relationships into a list of target channel': 'channellist.py',

    'Identify possible user associates via interaction network map': 'network.py',

    'Parse user messages to extract selectors/intel': 'selector.py',

    'Extract GPS data from collected user media': 'metadata.py',

    'Create visualization report from collected user messages': 'frequency.py',

    'Extract named entities from collected user messages': 'ner.py',

    'Conduct a subscriber census across a list of target channels': 'census.py',

    'Parse user messages to extract ideological indicators': 'indicators.py',
    
    'Parse user messages to extract indicators of capability and violent intent': 'assessment.py'
}


def display(options):
    for idx, option in enumerate(options.keys(), start=1):
        print(f"{idx}. {option}")


def get_choice(options):
    choose = int(input("\nPick a number: ")) - 1

    if choose < 0 or choose >= len(options):
        print('Invalid choice')

        return None

    return list(options.values())[choose]


display(options)

if choice := get_choice(options):
    # Stop any existing event loop

    stop_event_loop()

    print(f'Loading {choice}...')

    exec(open(choice).read())