import requests
from bs4 import BeautifulSoup
from colorama import Fore, Style
from datetime import datetime, timezone


def scrape_subscriber_counts(channel_urls):
    """
        Scrapes subscriber counts from a list of channel URLs and calculates the total number of subscribers.

        Args:
            channel_urls (list): List of URLs of the channels to scrape subscriber counts from.

        Returns:
            None

        Examples:
            scrape_subscriber_counts(["https://channel1.com", "https://channel2.com"])
    """
    total_subscribers = 0
    for url in channel_urls:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        if subscriber_count_element := soup.find(
                'div', class_='tgme_page_extra'
        ):
            subscriber_count_text = subscriber_count_element.text.strip()
            subscriber_count_parts = subscriber_count_text.split(',')
            member_count = subscriber_count_parts[0].strip()
            if subscriber_count := ''.join(
                    c for c in member_count if c.isdigit()
            ):
                print(
                    f"Channel: {Fore.BLUE + url + Style.RESET_ALL} | Members: {Fore.GREEN + subscriber_count + Style.RESET_ALL}")
                total_subscribers += int(subscriber_count)
            else:
                print(f"Channel: {Fore.BLUE + url + Style.RESET_ALL} | Member count not available")
        else:
            print(f"Channel: {Fore.BLUE + url + Style.RESET_ALL} | Member count not found")

    print(f"\nTotal Members: {total_subscribers}")
    current_time = datetime.now(timezone.utc).astimezone().strftime('%H:%M:%S, %d %B %Y %Z%z')
    print(f"Census Results as of {current_time}\n")
    print(
        f"{Fore.RED}Please Note: This total does not account for duplication. A single user may belong to multiple channels and therefore be included multiple times within this count.{Style.RESET_ALL}")


def main():
    """
        Reads a file containing a list of channel URLs, scrapes member counts for each channel, and prints the results.

        Returns:
            None

        Examples:
            main()
    """
    channel_urls_file = input("Enter the name of the file containing the list of channel URLs (csv or txt): ")

    # Read the channel URLs from the file
    with open(channel_urls_file) as file:
        channel_urls = [line.strip() for line in file if line.strip()]

    # Scrape member counts
    print("\nScraping member counts...\n")
    scrape_subscriber_counts(channel_urls)


if __name__ == "__main__":
    main()
