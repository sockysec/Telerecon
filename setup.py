from colorama import init, Fore, Style

# Function to update details.py file
def update_details_file(api_id, api_hash, phone_number):
    with open("details.py", "w") as file:
        file.write(f'apiID = "{api_id}"\n')
        file.write(f'apiHash = "{api_hash}"\n')
        file.write(f'number = "{phone_number}"\n')

# ask user for telegram details and guide them through it
init(autoreset=True)

print(Fore.CYAN + r' __________________________________________________________________')
print(Fore.CYAN + r'   _______ ______ _      ______ _____  ______ _____ ____  _   _    ')
print(Fore.CYAN + r'  |__   __|  ____| |    |  ____|  __ \|  ____/ ____/ __ \| \ | |   ')
print(Fore.CYAN + r'     | |  | |__  | |    | |__  | |__) | |__ | |   | |  | |  \| |   ')
print(Fore.CYAN + r'     | |  |  __| | |    |  __| |  _  /|  __|| |   | |  | | . ` |   ')
print(Fore.CYAN + r'     | |  | |____| |____| |____| | \ \| |___| |___| |__| | |\  |   ')
print(Fore.CYAN + r'     |_|  |______|______|______|_|  \_\______\_____\____/|_| \_| v2')
print(Fore.CYAN + r'___________________________________________________________________')
print(Style.RESET_ALL)

print('Welcome to the Telegram Scraper setup wizard.')
print('This file will insert your login information to the Telegram Scraper scripts.')
print('Follow the README instructions to get your credentials.')

while True:
    try:
        api_id = input("Please enter your API ID:\n")
        print(f'You entered "{api_id}"')
        confirmation = input('Is this correct? (y/n)')
        if confirmation.lower() == 'y':
            print('Updating...')
            break
    except:
        continue

while True:
    try:
        api_hash = input("Please enter your API Hash:\n")
        print(f'You entered "{api_hash}"')
        confirmation = input('Is this correct? (y/n)')
        if confirmation.lower() == 'y':
            print('Updating...')
            break
    except:
        continue

while True:
    try:
        phone_number = input("Please enter your phone number:\n")
        print(f'You entered "{phone_number}"')
        confirmation = input('Is this correct? (y/n)')
        if confirmation.lower() == 'y':
            print('Updating...')
            break
    except:
        continue

update_details_file(api_id, api_hash, phone_number)

print('Setup is complete.')

launcher = input('Do you want to open the launcher? (y/n)')

if launcher.lower() == 'y':
    print('Starting...')
    exec(open("launcher.py").read())
else:
    print('The launcher is now ready and can be started with the launcher.py file. You may now close the terminal.')