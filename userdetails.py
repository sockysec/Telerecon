import os

import datetime

from telethon import TelegramClient

from telethon.tl.types import UserStatusOffline

from colorama import init, Fore, Style

from details import apiID, apiHash, number

# Initialize colorama for colored console output

init(autoreset=True)


def format_timestamp(timestamp):
    return datetime.datetime.fromtimestamp(timestamp, datetime.timezone.utc).astimezone().strftime(
        '%Y-%m-%d %H:%M:%S %Z')


async def get_user_information(client, identifier, username):
    try:

        user = await client.get_entity(identifier)

        # Create a user-specific directory

        user_directory = os.path.join("Collection", username)

        if not os.path.exists(user_directory):
            os.makedirs(user_directory)

        print(f"{Fore.CYAN}Username:{Style.RESET_ALL} {user.username or 'N/A'}")

        print(f"{Fore.CYAN}First Name:{Style.RESET_ALL} {user.first_name or 'N/A'}")

        print(f"{Fore.CYAN}Last Name:{Style.RESET_ALL} {user.last_name or 'N/A'}")

        print(f"{Fore.CYAN}User ID:{Style.RESET_ALL} {user.id}")

        if user.phone:
            print(f"{Fore.CYAN}Phone Number:{Style.RESET_ALL} {user.phone}")

        if hasattr(user, 'about'):
            print(f"{Fore.CYAN}Bio:{Style.RESET_ALL} {user.about or 'N/A'}")

        if user.photo:

            profile_photo = await client.download_profile_photo(user.id, file=bytes)

            with open(os.path.join(user_directory, f'{username}_profile.jpg'), 'wb') as file:

                file.write(profile_photo)

            print(f"{Fore.CYAN}Profile Picture:{Style.RESET_ALL} Downloaded and saved as {username}_profile.jpg")

        else:

            print(f"{Fore.CYAN}Profile Picture:{Style.RESET_ALL} No")

        if user.status:

            if isinstance(user.status, UserStatusOffline):

                last_seen = user.status.was_online

                last_seen_formatted = format_timestamp(last_seen.timestamp())

                print(f"{Fore.CYAN}Last Seen:{Style.RESET_ALL} User was last seen at {last_seen_formatted}")

            else:

                print(f"{Fore.CYAN}Online Status:{Style.RESET_ALL} Online")

        else:

            print(f"{Fore.CYAN}Online Status:{Style.RESET_ALL} Offline")

        if hasattr(user, 'mutual_chats_count'):

            common_chats = user.mutual_chats_count

            if common_chats is not None:
                print(f"{Fore.CYAN}Common Chats:{Style.RESET_ALL} {common_chats}")

        # Save user details to a text file in the user-specific directory

        with open(os.path.join(user_directory, f'{username}_userdetails.txt'), 'w') as details_file:

            details_file.write(f"Username: {user.username or 'N/A'}\n")

            details_file.write(f"First Name: {user.first_name or 'N/A'}\n")

            details_file.write(f"Last Name: {user.last_name or 'N/A'}\n")

            details_file.write(f"User ID: {user.id}\n")

            if user.phone:
                details_file.write(f"Phone Number: {user.phone}\n")

            if hasattr(user, 'about'):
                details_file.write(f"Bio: {user.about or 'N/A'}\n")

            if user.status:

                if isinstance(user.status, UserStatusOffline):

                    last_seen = user.status.was_online

                    last_seen_formatted = format_timestamp(last_seen.timestamp())

                    details_file.write(f"Last Seen: User was last seen at {last_seen_formatted}\n")

                else:

                    details_file.write(f"Online Status: Online\n")

            else:

                details_file.write(f"Online Status: Offline\n")

            if hasattr(user, 'mutual_chats_count'):
                details_file.write(f"Common Chats: {common_chats}\n")



    except Exception as e:

        print(f"{Fore.RED}Error:{Style.RESET_ALL} {str(e)}")


async def main():
    identifier = input(f"{Fore.CYAN}Enter target @username{Fore.RESET}: ")

    # Create a 'Collection' directory if it doesn't exist

    if not os.path.exists("Collection"):
        os.makedirs("Collection")

    async with TelegramClient('session_name', apiID, apiHash) as client:

        # Remove "@" symbol from the username if present

        username = identifier.replace('@', '')

        # Call the function with the modified username

        await get_user_information(client, identifier, username)

    # Ask if the user wants to return to the launcher

    launcher = input('Do you want to return to the launcher? (y/n)')

    if launcher == 'y':
        print('Exiting...')

        # You can use 'os.system' to run the launcher script

        os.system('python3 launcher.py')


if __name__ == "__main__":
    asyncio.run(main())
