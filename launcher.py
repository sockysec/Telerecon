from telethon.sync import TelegramClient
from colorama import init, Fore, Style

# Initialize colorama
init(autoreset=True)

# Launcher code
print(Fore.CYAN + r' __________________________________________________________________')
print(Fore.CYAN + r'   _______ ______ _      ______ _____  ______ _____ ____  _   _    ')
print(Fore.CYAN + r'  |__   __|  ____| |    |  ____|  __ \|  ____/ ____/ __ \| \ | |   ')
print(Fore.CYAN + r'     | |  | |__  | |    | |__  | |__) | |__ | |   | |  | |  \| |   ')
print(Fore.CYAN + r'     | |  |  __| | |    |  __| |  _  /|  __|| |   | |  | | . ` |   ')
print(Fore.CYAN + r'     | |  | |____| |____| |____| | \ \| |___| |___| |__| | |\  |   ')
print(Fore.CYAN + r'     |_|  |______|______|______|_|  \_\______\_____\____/|_| \_| v2')
print(Fore.CYAN + r'___________________________________________________________________')
print(Style.RESET_ALL)

print(Fore.YELLOW + '                                          ')
print(Fore.YELLOW + 'Welcome to Telerecon, a scraper and reconnaissance framework for Telegram')
print(Fore.YELLOW + 'Please select an option:')
print(Style.RESET_ALL)

options = {
    'Get user information': 'target.py',
    'Check user activity across a list of channels': 'recon.py',
    'Collect user messages from a target channel': 'userscraper.py',
    'Collect user messages from a list of target channels': 'usermultiscraper.py',
    'Scrape all messages within a channel': 'channelscraper.py',
    'Scrape all t.me URL’s from within a channel': 'urlscraper.py',
    'Scrape forwarding relationships into target channel': 'channels.py',
    'Scrape forwarding relationships into a list of target channel': 'channellist.py',
    'Conduct a subscriber census across a list of target channels': 'census.py'
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
choice = get_choice(options)

if choice:
    print(f'Loading {choice}...')
    exec(open(choice).read())
