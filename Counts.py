import re
from datetime import datetime

def count_messages(file_path, start_date_str, end_date_str):
    # Convert start and end date strings to datetime objects
    start_date = datetime.strptime(start_date_str, "%m/%d/%y")
    end_date = datetime.strptime(end_date_str, "%m/%d/%y")

    # Dictionary to store sender counts
    sender_counts = {}

    # Open the file for reading
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

        # Iterate through each line in the file
        for line in lines:
            # Use regex to match message lines
            match = re.search(r"\[(\d{1,2}/\d{1,2}/\d{2,4}, \d{1,2}:\d{2}:\d{2})\] ([^:]+?): (.+)", line)

            if match:
                # Extract message date from the matched line
                message_date = datetime.strptime(match.group(1), "%m/%d/%y, %H:%M:%S")

                # Check if message date falls within the specified range
                if start_date <= message_date <= end_date:
                    name = match.group(2).strip()  # Extract sender's name
                    message = match.group(3).strip()  # Extract message content

                    # Count messages sent by each sender if the message content is less than 3 characters
                    if len(message) < 3:
                        sender_counts[name] = sender_counts.get(name, 0) + 1

    return sender_counts

# Example usage
file_path = 'file path '
start_date_str = '03/1/24'
end_date_str = '04/1/24'
result = count_messages(file_path, start_date_str, end_date_str)

# Sort the result by sender counts in descending order
sorted_result = dict(sorted(result.items(), key=lambda x: x[1], reverse=True))

# Print sender counts
for sender, count in sorted_result.items():
    print(f"{sender}: {count} ")
