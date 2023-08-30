from colorama import init, Fore, Style

#ask user for telegram details and guide them through it
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



fin1 = open("detailsshell.py", "rt")

fout1 = open("details.py", "wt")



while True:

    try:

        a = input("Please enter your API ID:\n")

        print(f'You entered "{a}"')

        a1 = input('Is this correct? (y/n)')

        if a1 == 'y':

            print('Updating...')

            new_text1 = a

            break;

    except:

            continue



while True:

    try:

        h = input("Please enter your API Hash:\n")

        print(f'You entered "{h}"')

        a2 = input('Is this correct? (y/n)')

        if a2 == 'y':

            print('Updating...')

            new_text2 = "'" + h + "'"

            break;

    except:

            continue



while True:

    try:

        n = input("Please enter your phone number:\n")

        print(f'You entered "{n}"')

        a3 = input('Is this correct? (y/n)')

        if a3 == 'y':

            print('Updating...')

            new_text3 = "'" + n + "'"

            break;

    except:

            continue



checkWords = ("old_text1","old_text2","old_text3")

repWords = (new_text1,new_text2,new_text3)



for line in fin1:

    for check, rep in zip(checkWords, repWords):

        line = line.replace(check, rep)

    fout1.write(line)



fin1.close()

fout1.close()



print('Setup is complete.')



launcher = input('Do you want to open the launcher? (y/n)')

if launcher == 'y':

    print('Starting...')

    exec(open("launcher.py").read())

else:

    print('The launcher is now ready and can be started with the launcher.py file. You may now close the terminal.')
