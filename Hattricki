import re
from datetime import datetime

def find_hattricks(file_path, start_date_str, end_date_str):
    # Convert start and end date strings to datetime objects
    start_date = datetime.strptime(start_date_str, "%m/%d/%y")
    end_date = datetime.strptime(end_date_str, "%m/%d/%y")

    previous_sender = None  # Initialize variable to store the previous sender
    consecutive_messages = 0  # Initialize counter for consecutive single character messages
    hattricks = []  # List to store hattricks

    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

        for line in lines:
            # Use regex to match message lines and extract message date, sender, and content
            match = re.search(r"\[(\d{1,2}/\d{1,2}/\d{2,4}, \d{1,2}:\d{2}:\d{2})\] ([^:]+?): (.+)", line)

            if match:
                message_date = datetime.strptime(match.group(1), "%m/%d/%y, %H:%M:%S")

                # Check if message date falls within the specified range
                if start_date <= message_date <= end_date:
                    sender = match.group(2).strip()
                    message = match.group(3).strip()

                    # Count consecutive single character messages by the same sender
                    if len(message) == 1:
                        if sender == previous_sender:
                            consecutive_messages += 1
                            if consecutive_messages == 3:
                                hattricks.append((sender, message_date))  # Store hattrick sender and date
                                consecutive_messages = 0  # Reset consecutive count for potential subsequent hattricks
                        else:
                            consecutive_messages = 1
                            previous_sender = sender
                    else:
                        consecutive_messages = 0  # Reset consecutive count if message is longer than 1 character

    return hattricks

# File path and date range for analyzing hattricks
file_path = 'file path'
start_date_str = '03/1/24'
end_date_str = '04/1/24'

# Find hattricks within the specified date range
hattricks = find_hattricks(file_path, start_date_str, end_date_str)

# Display hattricks if found, otherwise indicate no hattricks were found
if hattricks:
    print("Hattricks found:")
    for hattrick in hattricks:
        print(f"{hattrick[0]} achieved a hattrick at {hattrick[1]}")
else:
    print("No hattricks found.")
