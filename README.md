# Telerecon
A reconnaissance framework for researching and investigating Telegram for OSINT purposes.

![image](https://github.com/sockysec/Telerecon/assets/121141737/34b07f2f-54ab-4598-95fd-22faca80cfd3)


# Installation 

1. Download all files and save to directory of choice.

2. Navigate to the primary Telerecon directory and install the requirements.
```
pip install -r requirements.txt
```

3. Obtain your Telegram API details from my.telegram.org noting your API key, hash, and phone number.
4. In terminal, navigate to the installation directory (eg, Telerecon-main) and run setup.py
```
python3 setup.py
```
5. As prompted by the script, input your Telegram API key, hash, and phone number (these details will be saved locally).
6. Telegram may message you a verification code, to confirm setup. If so input the verification code.
7. If prompted to "Please enter your phone (or bot token):" then you may need to re-input your account phone number. Telegram will then message you the code (in Telegram) to verify your login "Please enter the code you received:".

8. Telerecon is now installed, run launcher.py to use.


#Use

1. Run launcher.py
```
python3 launcher.py
```
2. Select an option from the menu


# Example Targeting Workflow

Directory creation - Telerecon allows you to search across multiple channels and groups for a target user's activity/posts. However, this requires the creation of a directory of target Telegram channels to search across (Ex. This may be all chats in a geographic area or a target ideological grouping.). If you know the URLs of specific channels, you can manually create your own directory by simply making a csv/txt file with the list of target Telegram URL's on each line. Option '6' can allow you to scrape URLs from pre-existing Telegram directories (i.e. nzdirectory) to quickly build a list. Option '7' utilizes exploratory forward mapping to discover related channels/chat groups and produce a list. Option '8' can be used for a more comprehensive list.

1. Run launcher.py
2. Select '1' and input a target username (i.e. @Johnsmith), return to the launcher
3. Select '2', input target username (i.e. @Johnsmith), input target channel list (i.e. targetchats.txt)
4. When asked whether you would like to scrape posts, select 'y'. Alternatively, select '4'.
5. Input target username (i.e. @Johnsmith) and channel list (i.e. targetchats.txt). Choose whether or not to include media (media will take longer). After running, return to After running,  launcher.
6. Select '9', input target username (i.e. @Johnsmith). After running, return to the launcher.
7. Select '10', input target username (i.e. @Johnsmith) and define a timezone. After running, to the launcher.
8. Select '11', input target username (i.e. @Johnsmith). After running, return to the launcher.

Output - 
- Public User Information (username, first name, last name, phone number, UserID, Bio, Online status, profile picture).
- User activity across target channels/groups.
- All posts/messages/media posted by that user across target channels/groups.
- Comprehensive analytics report showing user postage patterns (useful for pattern of life analysis etc).
- A compiled spreadsheet of extracted EXIF metadata from all images, and a map visualization displaying any extracted GPS metadata.
- A report containing extracted Person, Organisation, Location, and date entities extracted by named entity recognition
- A report containing any possible Phone numbers, email addresses, domains, and usernames mentioned (report includes citations for ease of verification)

..............

# Known Issues
- UserID inputs are not currently working.
- Current media download method does not retain image EXIF metadata.

..............

# Credit

Credit to Jordan Wildon's (@jordanwildon) Telegram Scraper for the initial inspiration. https://github.com/TechRahul20/TelegramScraper

..............

# MIT License

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions: The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
