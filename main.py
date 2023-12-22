import requests
import os
from dotenv import load_dotenv
from twilio.rest import Client
import time
from bs4 import BeautifulSoup

# Load environment variables from .env file
load_dotenv()

# Twilio credentials
account_sid = os.getenv('TWILIO_ACCOUNT_SID')
auth_token = os.getenv('TWILIO_AUTH_TOKEN')
twilio_phone_number = os.getenv('TWILIO_PHONE_NUMBER')
destination_phone_number = os.getenv('DESTINATION_PHONE_NUMBER')
website_url = os.getenv('WEBSITE')
TEST_PROGRAM = os.getenv('TEST_PROGRAM')

TEST_PROGRAM = TEST_PROGRAM.lower() == 'true'

# Website to monitor
previous_content = None
previous_images = None

# Twilio client
client = Client(account_sid, auth_token)

def extract_text_from_html(html):
    soup = BeautifulSoup(html, 'html.parser')
    text = ' '.join([tag.get_text(strip=True) for tag in soup.find_all(['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6'])])
    return text

def extract_images_from_html(html):
    soup = BeautifulSoup(html, 'html.parser')
    images = [img.get('src') for img in soup.find_all('img') if img.get('src')]
    return images


def check_website():
    global previous_content, previous_images

    # Fetch website content
    response = requests.get(website_url)
    current_html_content = response.text

    # Extract text from specific HTML elements
    current_content = extract_text_from_html(current_html_content)

    # Extract image URLs
    current_images = extract_images_from_html(current_html_content)

    if TEST_PROGRAM:
        print('checking')

    # Check if this is the first check
    if previous_content is None and previous_images is None:
        if TEST_PROGRAM:
            print("Initial check. No differences to display.")
    else:
        # Compare content with the previous check
        if current_content != previous_content or current_images != previous_images:
            # Website has been updated
            send_notification()
        else:
            if TEST_PROGRAM:
                print("No update detected.")

    # Update previous_content and previous_images regardless of update
    previous_content = current_content
    previous_images = current_images

def send_notification():
    message = client.messages.create(
        body=f'The website {website_url} has been updated!',
        from_=twilio_phone_number,
        to=destination_phone_number
    )
    if TEST_PROGRAM:
        print(f"Notification sent! SID: {message.sid}")

if __name__ == "__main__":
    while True:
        check_website()
        if TEST_PROGRAM:
            time.sleep(10)
        else:
            # Wait for an hour before checking again
            time.sleep(3600)
