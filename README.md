# Telerecon
Telerecon is a reconnaissance framework for researching and investigating Telegram for OSINT purposes.

![image](https://github.com/sockysec/Telerecon/assets/121141737/096861e9-5f4d-42cb-8360-9a59676460ce)


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


# Use

1. Run launcher.py
```
python3 launcher.py
```
2. Select an option from the menu

# Options

1. **Get user information:**  search a @username and return any public user information (username, first name, last name, phone number, UserID, Bio, Online status, profile picture).

2. **Check user activity across a list of channels:**  iterate through a txt/csv directory list of Telegram channels, looking for any messages by the target username. (Assumes directory list is in the primary Telerecon directory).

3. **Collect user messages from a target channel:**  collect and compile any messages from the target username in a target channel. Option to also download media. 

4. **Collect user messages from a list of target channels:**  iterate through a txt/csv directory list of Telegram channels, collecting and compiling any messages by the target username. Option to also download media. (Assumes directory list is in the primary Telerecon directory).

5. **Scrape all messages within a channel:**  collect and compile messages in a target channel. Download full history, last 24 hours, or custom date range.

6. **Scrape all t.me URL’s from within a channel:**  parses a channel and extracts all t.me URLs mentioned within. This is designed to easily create a Telegram directory.

7. **Scrape forwarding relationships into target channel:**  scrape forwarding relationships into a target channel. Exporting a Gephi optimised adjacency list, and URL directory of the discovered channels.

8. **Scrape forwarding relationships into a list of target channel:** iterate through a txt/csv directory list of Telegram channels, scraping forwarding relationship. Exporting a Gephi optimised adjacency list, and URL directory of the discovered channels. Afterwards can use terminal commands to merge outputs. (i.e. merge URLs lists = cat *.csv | sort | uniq > combined.csv)

9. **Identify possible user associates via interaction network map:** assumes user messages have already been collected. Constructs a network visualisation showing replies/interactions with other users (useful for identifying possible associates).  

10. **Parse user messages to extract selectors/intel:** outputting a report containing any potential phone numbers, emails, or other selectors based on regex and key phrase targeting (the report includes citations for ease of verification). Key phrases are customizable by editing the script.

11. **Extract GPS data from collected user media:** assumes user messages have already been collected. Creates a compiled spreadsheet of extracted EXIF metadata from all images, and a map visualization displaying any extracted GPS metadata.

12. **Create visulisation report from collected user messages:** assumes user messages have already been collected. Creates a comprehensive analytics report showing user postage patterns over time (useful for pattern of life analysis etc).

13. **Extract named entities from collected user messages:** assumes user messages have already been collected. Creates a report containing extracted Person, Organisation, Location, and date entities extracted by named entity recognition.

14. **Conduct a subscriber census across a list of target channels:** iterate through a txt/csv directory list of Telegram channels, reporting the number of subscribers/members.


# Example Targeting Workflow

**Directory creation** - Telerecon allows you to search across multiple channels and groups for a target user's activity/posts. However, this requires the creation of a directory of target Telegram channels to search across (Ex. This may be all chats in a geographic area or a target ideological grouping.). If you know the URLs of specific channels, you can manually create your own directory by simply making a csv/txt file with the list of target Telegram URL's on each line. Option '6' can allow you to scrape URLs from pre-existing Telegram directories (i.e. nzdirectory) to quickly build a list. Option '7' utilizes exploratory forward mapping to discover related channels/chat groups and produce a list. Option '8' can be used for a more comprehensive list.

Targeting
1. Run launcher.py
2. Select '1' and input a target username (i.e. @Johnsmith), return to the launcher
3. Select '2', input target username (i.e. @Johnsmith), input target channel list (i.e. targetchats.txt)
4. When asked whether you would like to scrape posts, select 'y'. Alternatively, select '4'. Input target username (i.e. @Johnsmith) and channel list (i.e. targetchats.txt). Choose whether or not to include media (media will take longer). After running, return to the launcher.
5. Select '9', input target username (i.e. @Johnsmith). After running, return to the launcher.
6. Select '10', input target username (i.e. @Johnsmith). After running, to the launcher.
7. Select '11', input target username (i.e. @Johnsmith). After running, to the launcher.
8. Select '12', input target username (i.e. @Johnsmith) and define a timezone. After running, return to the launcher.
7. Select '13', input target username (i.e. @Johnsmith). After running, return to the launcher.
   

# Usage Notes

- Running the advanced reports and analytics (9, 10, 11, 12, 13) assume that you have already collected the target user's posts.


# Known Issues
- Currently the media download method does not retain image EXIF metadata, meaning that GPS/EXIF extraction function will return blank.



# Credit

Credit to Jordan Wildon's (@jordanwildon) Telegram Scraper for the initial inspiration. https://github.com/TechRahul20/TelegramScraper



# MIT License

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions: The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
