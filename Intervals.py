import re
from datetime import datetime, timedelta

def count_messages_by_user_and_interval(file_path, start_date_str, end_date_str):
    # Convert start and end date strings to datetime objects
    start_date = datetime.strptime(start_date_str, "%m/%d/%y")
    end_date = datetime.strptime(end_date_str, "%m/%d/%y")

    sender_interval_counts = {}  # Dictionary to store message counts by user and time interval

    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

        for line in lines:
            match = re.search(r"\[(\d{1,2}/\d{1,2}/\d{2,4}, \d{1,2}:\d{2}:\d{2})\] ([^:]+?): (.+)", line)

            if match:
                message_date_str = match.group(1)
                name = match.group(2).strip()

                # Adjust message date for specific users and time zones
                if name.startswith('T'):
                    message_date = datetime.strptime(message_date_str, "%m/%d/%y, %H:%M:%S") - timedelta(hours=3)
                elif name.startswith('G'):
                    message_date = datetime.strptime(message_date_str, "%m/%d/%y, %H:%M:%S") + timedelta(hours=6)
                else:
                    message_date = datetime.strptime(message_date_str, "%m/%d/%y, %H:%M:%S")

                # Check if message date falls within the specified range
                if start_date <= message_date <= end_date:
                    if 3 <= len(name) <= 40:  # Validate the length of the sender's name

                        # Determine time of day interval for the message
                        time_of_day = message_date.strftime("%H:%M:%S")
                        interval_key = None

                        if "00:00:00" <= time_of_day <= "05:59:00":
                            interval_key = "00:00-05:59"
                        elif "06:00:00" <= time_of_day <= "11:59:00":
                            interval_key = "06:00-11:59"
                        elif "12:00:00" <= time_of_day <= "17:59:00":
                            interval_key = "12:00-17:59"
                        elif "18:00:00" <= time_of_day <= "23:59:00":
                            interval_key = "18:00-23:59"

                        # Update message count for the sender and interval
                        if name not in sender_interval_counts:
                            sender_interval_counts[name] = {interval_key: 1}
                        else:
                            if interval_key not in sender_interval_counts[name]:
                                sender_interval_counts[name][interval_key] = 1
                            else:
                                sender_interval_counts[name][interval_key] += 1

    return sender_interval_counts

def calculate_percentage(sender_interval_counts):
    sender_percentage = {}  # Dictionary to store message percentage by user and interval

    for sender, intervals in sender_interval_counts.items():
        total_messages = sum(intervals.values())  # Calculate total messages sent by the user

        # Filter out intervals with None values and calculate percentage for each interval
        valid_intervals = {interval: count for interval, count in intervals.items() if interval is not None}
        percentage_intervals = {interval: count / total_messages * 100 for interval, count in valid_intervals.items()}
        sender_percentage[sender] = percentage_intervals

    return sender_percentage

# File path and date range for analyzing message counts
file_path = ' file path '
start_date_str = '03/1/24'
end_date_str = '04/1/24'

# Get message counts by user and time interval
sender_interval_counts = count_messages_by_user_and_interval(file_path, start_date_str, end_date_str)

# Calculate message percentage by user and time interval
sender_percentage = calculate_percentage(sender_interval_counts)

# Display message statistics
print("Dookie Stats:")
for sender, percentages in sender_percentage.items():
    print(f"\n{sender}:")
    for interval, percentage in percentages.items():
        print(f"  {interval}: {percentage:.2f}%")
