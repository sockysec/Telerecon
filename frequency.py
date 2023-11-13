import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from pytz import timezone
from tzlocal import get_localzone  # Added to get the system's local timezone

# Load the CSV file into a pandas DataFrame based on the target username
target_username = input("Enter the target username: ")
csv_file = f'Collection/{target_username.strip("@")}/{target_username.strip("@")}_messages.csv'
df = pd.read_csv(csv_file)

# Input for custom timezone
custom_timezone = input("Enter a custom timezone (e.g., 'Pacific/Auckland'): ")

# Convert the 'Date' column to a datetime object and convert to the custom timezone
df['Date'] = pd.to_datetime(df['Date'], format='%Y-%m-%d %H:%M:%S%z')
try:
    custom_tz = timezone(custom_timezone)
    df['Date'] = df['Date'].dt.tz_convert(custom_tz)
except Exception as e:
    print(f"Error: {e}. Using the system's local timezone instead.")
    local_tz = get_localzone()
    df['Date'] = df['Date'].dt.tz_convert(local_tz)

# Group data by user and hour, and count the frequency of posts
df_grouped_hourly = df.groupby([df['Date'].dt.hour, 'Username']).size().reset_index(name='post_count')

# Pivot the data for the first graph (hourly posting patterns)
pivot_hourly = df_grouped_hourly.pivot(index='Date', columns='Username', values='post_count').fillna(0)

# Group data by user and date, and sum the daily post counts
df_grouped_daily = df.groupby([df['Date'].dt.date, 'Username']).size().reset_index(name='post_count')

# Pivot the data for the second graph (daily posting patterns)
pivot_daily = df_grouped_daily.pivot(index='Date', columns='Username', values='post_count').fillna(0)

# Calculate posting frequency based on the day of the week
df['DayOfWeek'] = df['Date'].dt.day_name()
df_grouped_dayofweek = df.groupby(['DayOfWeek', 'Username']).size().reset_index(name='post_count_dayofweek')
desired_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
pivot_dayofweek = df_grouped_dayofweek.pivot(index='DayOfWeek', columns='Username',
                                             values='post_count_dayofweek').fillna(0)

# Reorder the days of the week
pivot_dayofweek = pivot_dayofweek.reindex(desired_order, axis=0)

# Calculate posting frequency based on the day of the month
df['DayOfMonth'] = df['Date'].dt.day
df_grouped_dayofmonth = df.groupby(['DayOfMonth', 'Username']).size().reset_index(name='post_count_dayofmonth')

# Pivot the data for the third graph (posting frequency by day of the month)
pivot_dayofmonth = df_grouped_dayofmonth.pivot(index='DayOfMonth', columns='Username',
                                               values='post_count_dayofmonth').fillna(0)

# Convert non-string values in 'Text' column to string
df['Text'] = df['Text'].astype(str)

# Save the visualizations to a single PDF in the target user's directory
output_pdf = f'Collection/{target_username.strip("@")}/visualization_report_{target_username.strip("@")}.pdf'
with PdfPages(output_pdf) as pdf:
    # First graph (hourly posting patterns)
    plt.figure(figsize=(10, 5))
    pivot_hourly.plot(kind='bar', stacked=True)
    plt.title('Users Posting Patterns Over a 24-Hour Period')
    plt.xlabel('Hour of the Day')
    plt.ylabel('Post Count')
    plt.legend(title='Users')
    plt.grid(True)
    plt.xticks(rotation=0)
    plt.tight_layout()
    pdf.savefig()

    # Second graph (daily posting patterns)
    plt.figure(figsize=(10, 5))
    pivot_daily.plot(kind='line')
    plt.title('Users Posting Patterns Over Time (Summed Daily)')
    plt.xlabel('Date')
    plt.ylabel('Post Count')
    plt.legend(title='Users')
    plt.grid(True)
    plt.tight_layout()
    pdf.savefig()

    # Third graph (posting frequency by day of the week)
    plt.figure(figsize=(10, 5))
    pivot_dayofweek.plot(kind='bar', stacked=True)
    plt.title('Users Posting Patterns by Day of the Week')
    plt.xlabel('Day of the Week')
    plt.ylabel('Post Count')
    plt.legend(title='Users')
    plt.grid(True)
    plt.xticks(rotation=0)
    plt.tight_layout()
    pdf.savefig()

    # Fourth graph (posting frequency by day of the month)
    plt.figure(figsize=(10, 5))
    pivot_dayofmonth.plot(kind='bar', stacked=True)
    plt.title('Users Posting Patterns by Day of the Month')
    plt.xlabel('Day of the Month')
    plt.ylabel('Post Count')
    plt.legend(title='Users')
    plt.grid(True)
    plt.xticks(rotation=0)
    plt.tight_layout()
    pdf.savefig()

print(f"PDF report created: {output_pdf}")

# Ask if the user wants to return to the launcher
launcher = input('Do you want to return to the launcher? (y/n)')

if launcher == 'y':
    print('Restarting...')
    exec(open("launcher.py").read())
