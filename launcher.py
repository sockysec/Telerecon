import asyncio
import importlib
from colorama import init, Fore, Style

def print_logo():
    # Initialize colorama
    init(autoreset=True)

    # Launcher code
    print(f'{Fore.CYAN} __________________________________________________________________')
    print(f'{Fore.CYAN}   _______ ______ _      ______ _____  ______ _____ ____  _   _    ')
    print(Fore.CYAN + r'  |__   __|  ____| |    |  ____|  __ \|  ____/ ____/ __ \| \ | |   ')
    print(Fore.CYAN + r'     | |  | |__  | |    | |__  | |__) | |__ | |   | |  | |  \| |   ')
    print(f'{Fore.CYAN}     | |  |  __| | |    |  __| |  _  /|  __|| |   | |  | | . ` |   ')
    print(Fore.CYAN + r'     | |  | |____| |____| |____| | \ \| |___| |___| |__| | |\  |   ')
    print(Fore.CYAN + r'     |_|  |______|______|______|_|  \_\______\_____\____/|_| \_| v2.1')
    print(f'{Fore.CYAN}___________________________________________________________________')
    print(Style.RESET_ALL)
    print(f'{Fore.YELLOW}                                          ')
    print(f'{Fore.YELLOW}Welcome to Telerecon, a scraper and reconnaissance framework for Telegram')
    print("")
    print(f'{Fore.YELLOW}Please select an option:')
    print(Style.RESET_ALL)

def display(options):
        for idx, option in enumerate(options.keys(), start=1):
            print(f"{idx}. {option}")

def get_choice(options):
    while True:
        display(options)
        choose = int(input("\nPick a number: ")) - 1

        if choose < 0 or choose >= len(options):
            print('Invalid choice')
        else:
            return list(options.values())[choose]

def load_and_run_module(choice):
        try:
            print(choice)
            module = importlib.import_module(choice)
            if choice in ('channels', 'channellist', 'userscraper', 'usermultiscraper', 'userdetails', 'urlscraper', 'recon', 'channelscraper'):
                asyncio.run(module.main())
            else:
                module.main()

            # Ask if the user wants to return to launcher
            launcher = input('Do you want to return to the launcher? (y/n)')
            if launcher.lower() == 'n':
                return False

        except ImportError:
            print(f'Failed to load {choice}')

        return True

def main():
    options = {
        'Get user information': 'userdetails',
        'Check user activity across a list of channels': 'recon',
        'Collect user messages from a target channel': 'userscraper',
        'Collect user messages from a list of target channels': 'usermultiscraper',
        'Scrape all messages within a channel': 'channelscraper',
        'Scrape all t.me URL’s from within a channel': 'urlscraper',
        'Scrape forwarding relationships into a target channel': 'channels',
        'Scrape forwarding relationships into a list of target channel': 'channellist',
        'Identify possible user associates via interaction network map': 'network',
        'Parse user messages to extract selectors/intel': 'selector',
        'Extract GPS data from collected user media': 'metadata',
        'Create visualization report from collected user messages': 'frequency',
        'Extract named entities from collected user messages': 'ner',
        'Conduct a subscriber census across a list of target channels': 'census',
        'Parse user messages to extract ideological indicators': 'indicators',
        'Parse user messages to extract indicators of capability and violent intent': 'assessment'
    }

    while True:
        print_logo()

        if choice := get_choice(options):
            print(f'Loading {choice}...')
            if not load_and_run_module(choice):
                break

main()