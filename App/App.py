from rich import text
from rich import box
from rich import print
from rich.panel import Panel
from rich.traceback import install
install(show_locals=True)

import pandas as pd
import requests
from bs4 import BeautifulSoup
import re
from instagrapi import Client
from instagrapi.exceptions import UserNotFound, LoginRequired
import logging
from mailjet_rest import Client as MailjetClient
import time

# Setup logging
logger = logging.getLogger()

# Load the CSV file
file_path = 'Examplar Prospects List.csv'
df = pd.read_csv(file_path)

# Assuming the website links are in column 'F'
websites = df.iloc[:, 5]  # Adjust the column index as necessary

# Instagrapi client setup
cl = Client()
cl.delay_range = [45, 50]  # Set delay range for requests

# Replace these with your actual username and password
USERNAME = "ig_user"
PASSWORD = "ig_pass"

# Mailjet setup
mailjet_api_key = 'mailjet_api_key'
mailjet_api_secret = 'mailjet_secret_key'
mailjet_client = MailjetClient(auth=(mailjet_api_key, mailjet_api_secret), version='v3.1')

def login_user():
    """
    Login to Instagram with username and password.
    """
    try:
        if cl.login(USERNAME, PASSWORD):
            logger.info("Logged in successfully.")
    except Exception as e:
        logger.error(f"Login failed: {e}")
        raise Exception("Login failed")

login_user()

def scrape_facebook_and_gmail(websites):
    facebook_links = []
    gmail_addresses = []

    for url in websites:
        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                links = soup.find_all('a', href=True)
                for link in links:
                    href = link['href']
                    if "facebook.com" in href:
                        facebook_links.append(href)
                text = soup.get_text()
                gmail_addresses.extend(re.findall(r"[a-zA-Z0-9_.+-]+@gmail.com", text))
        except requests.RequestException as e:
            logger.error(f"Error fetching {url}: {e}")
    
    # Print all Facebook links
    print(Panel.fit("\n".join(facebook_links), title="Facebook Links", border_style="bold blue", box=box.SQUARE))
    # Print all Gmail addresses
    print(Panel.fit("\n".join(gmail_addresses), title="Gmail Addresses", border_style="bold magenta", box=box.SQUARE))

    # Email sending to the scraped Gmail addresses
    for email in gmail_addresses:
        send_email(email)

def send_email(recipient_email):
    data = {
      'Messages': [
        {
          "From": {
            "Email": "wordsmithscript@gmail.com",
            "Name": "WordSmith Agency"
          },
          "To": [
            {
              "Email": recipient_email,
              "Name": "Valued Prospect"
            }
          ],
          "Subject": "Unlocking Potential with WordSmith Agency",
          "TextPart": "Greetings, We've noticed your potential and we're excited to offer our services to help elevate your business. Let's connect for a transformative collaboration.",
          "HTMLPart": "<h3>Ready to Elevate Your Business?</h3><p>We at WordSmith Agency are thrilled at the prospect of working with you. Let's make something great together.</p>",
          "CustomID": "AppGettingStartedTest"
        }
      ]
    }
    result = mailjet_client.send.create(data=data)
    if result.status_code == 200:
        print(Panel.fit(f"Email successfully sent to {recipient_email}", border_style="bold green", box=box.SQUARE))
    else:
        print(Panel.fit(f"Failed to send email to {recipient_email}. Error: {result.json()}", border_style="bold red", box=box.SQUARE))

def send_instagram_message(websites):
    messages_sent = 0
    for url in websites:
        if messages_sent >= 15:
            break  # Stop sending messages after 18
        found_instagram = False
        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                links = soup.find_all('a', href=True)
                for link in links:
                    href = link['href']
                    if "instagram.com" in href:
                        username = extract_instagram_username(href)
                        if username:
                            found_instagram = True
                            try:
                                user_id = cl.user_id_from_username(username)
                                message = f"Hey {username},\n\nImpressed by the range of services, especially as summer heats up the demand. We offer expert digital marketing with a twist: no payment until you see results. Ready to make this summer your most profitable one? Let's chat."
                                cl.direct_send(message, [user_id])
                                messages_sent += 1
                                break  # Move to next website after sending a message
                            except UserNotFound:
                                print(Panel.fit(f"Instagram user {username} not found. Skipping...", border_style="bold yellow", box=box.SQUARE))
            else:
                print(Panel.fit(f"Could not retrieve {url}", border_style="bold red", box=box.SQUARE))
        except requests.RequestException as e:
            print(Panel.fit(f"Error: {e}", border_style="bold red", box=box.SQUARE))

def extract_instagram_username(instagram_url):
    match = re.search(r"instagram.com/([^/?#&]+)", instagram_url)
    if match:
        return match.group(1)
    else:
        return None

# Implementation 
send_instagram_message(websites)
scrape_facebook_and_gmail(websites)