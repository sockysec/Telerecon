import datetime
from telethon.sync import TelegramClient
from telethon.tl.types import UserStatusOffline
from colorama import init, Fore
from details import apiID, apiHash, number

# Initialize colorama for colored console output
init(autoreset=True)

def format_timestamp(timestamp):
    return datetime.datetime.fromtimestamp(timestamp, datetime.timezone.utc).astimezone().strftime('%Y-%m-%d %H:%M:%S %Z')

def get_user_information(client, identifier):
    try:
        user = client.get_entity(identifier)
        print("Username:", Fore.CYAN + (user.username or "N/A"))
        print("First Name:", Fore.CYAN + (user.first_name or "N/A"))
        print("Last Name:", Fore.CYAN + (user.last_name or "N/A"))
        print("User ID:", Fore.CYAN + str(user.id))
        
        if user.phone:
            print("Phone Number:", Fore.CYAN + user.phone)
        if hasattr(user, 'about'):
            print("Bio:", Fore.CYAN + (user.about or "N/A"))
        
        if user.photo:
            username = user.username or user.id
            profile_photo = client.download_profile_photo(user.id, file=bytes)
            with open(f'{username}.jpg', 'wb') as file:
                file.write(profile_photo)
            print("Profile Picture:", Fore.CYAN + f"Downloaded and saved as {username}.jpg")
        else:
            print("Profile Picture:", Fore.CYAN + "No")
        
        if user.status:
            if isinstance(user.status, UserStatusOffline):
                last_seen = user.status.was_online
                last_seen_formatted = format_timestamp(last_seen.timestamp())
                print("Last Seen:", Fore.CYAN + f"User was last seen at {last_seen_formatted}")
            else:
                print("Online Status:", Fore.GREEN + "Online")
        else:
            print("Online Status:", Fore.RED + "Offline")
        
        if hasattr(user, 'mutual_chats_count'):
            common_chats = user.mutual_chats_count
            if common_chats is not None:
                print("Common Chats:", Fore.CYAN + str(common_chats))
            
    except Exception as e:
        print("Error:", Fore.RED + str(e))

if __name__ == "__main__":
    identifier = input("Enter target (@username, user ID, or phone number i.e. +1234567890 ): ")
    
    with TelegramClient('session_name', apiID, apiHash) as client:
        get_user_information(client, identifier)
