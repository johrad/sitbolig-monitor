import requests
import time
from datetime import datetime
import random
from playsound import playsound

# Define a list of websites to monitor (replace with your own URLs)
websites = [
    'https://folk.ntnu.no/jpdragic/',
    'https://bolig.sit.no/en/unit/hk46-41'
]

# Initialize a dictionary to store the previous content and timestamp for each website
previous_data = {url: {'content': '', 'timestamp': None} for url in websites}

# Define the filename for the log file
log_file = 'website_update_log_MONITOR.txt'

nChecks = 0
print("running..")
while True:
    try:
        for url in websites:
            time.sleep(random.randint(2, 4))
            # Make a GET request to the website
            response = requests.get(url)
            response.raise_for_status()  # Raise an exception for bad requests

            # Get the current content of the website
            current_content = response.text
            print(current_content)
            # Check if the content has changed
            if current_content != previous_data[url]['content']:
                # Get the current timestamp
                current_timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                update_message = f"Website '{url}' content has been updated at {current_timestamp}!"

                # Update the previous content and timestamp for this website
                previous_data[url]['content'] = current_content
                previous_data[url]['timestamp'] = current_timestamp

                if nChecks > 0:
                    # Print the update message to the terminal
                    print(update_message)

                    playsound('alarm1.wav')

                    # Save the update message to the log file
                    with open(log_file, 'a') as file:
                        file.write(update_message + '\n' +
                                   current_content + '\n')

            # Wait for a specific interval before checking again
        # Check every n seconds (randomized to avoid rate limiting)
        nChecks += 1
        with open(log_file, 'a') as file:
            file.write(f'nUpdates:{nChecks}' + '\n')
        time.sleep(random.randint(104, 353))

    except Exception as e:
        error_message = f"An error occurred: {e}"
        print(error_message)

        # Save the error message to the log file
        with open(log_file, 'a') as file:
            file.write(error_message + '\n')
