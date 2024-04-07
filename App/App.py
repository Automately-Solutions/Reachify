from rich import print, box
from rich.panel import Panel
from rich.traceback import install
install(show_locals=True)

import pandas as pd
import requests
from bs4 import BeautifulSoup
import re
from instagrapi import Client, exceptions
import logging

# Setup logging
logger = logging.getLogger()

# Load the .csv file using pandas
file_path = 'Examplar Prospects List.csv'
df = pd.read_csv(file_path)  # Change to read_csv for CSV files

# Assuming the website links are in column 'F'
websites = df.iloc[:, 5]  # Adjust the column index as necessary

# Instagrapi client setup with proxy
cl = Client()

cl.delay_range = [10, 15]  # Set delay range for requests

# Replace these with your actual username and password
USERNAME = "wordsmith.agency"
PASSWORD = "wordsmithscriptsforyou"

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

def extract_instagram_username(instagram_url):
    match = re.search(r"instagram.com/([^/?#&]+)", instagram_url)
    if match:
        return match.group(1)
    else:
        return None

facebook_links = []
gmail_addresses = []
messages_sent = 0

def process_websites(websites, df):
    global messages_sent
    for index, url in websites.iteritems():
        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                links = soup.find_all('a', href=True)
                for link in links:
                    href = link['href']
                    if "facebook.com" in href:
                        facebook_links.append(href)
                    if "instagram.com" in href:
                        username = extract_instagram_username(href)
                        if username:
                            try:
                                user_id = cl.user_id_from_username(username)
                                message = f"Hey {username},\n\nImpressed by the range of services, especially as summer heats up the demand. At Pixelevate, we offer expert digital marketing with a twist: no payment until you see results. Ready to make this summer your most profitable one? Let's chat."
                                cl.direct_send(message, [user_id])
                                df.at[index, 'Status'] = 'Done'  # Update the status in the DataFrame
                                messages_sent += 1
                                print(Panel.fit(f"Message sent to {username}", border_style="bold green", box=box.SQUARE))
                                break
                            except exceptions.UserNotFound:
                                print(Panel.fit(f"Instagram user {username} not found. Skipping...", border_style="bold yellow", box=box.SQUARE))
                                df.at[index, 'Status'] = 'Pending'
                text = soup.get_text()
                gmail_addresses.extend(re.findall(r"[a-zA-Z0-9_.+-]+@gmail.com", text))
            else:
                print(Panel.fit(f"Could not retrieve {url}", border_style="bold red", box=box.SQUARE))
                df.at[index, 'Status'] = 'Pending'
        except requests.RequestException as e:
            print(Panel.fit(f"Error: {e}", border_style="bold red", box=box.SQUARE))
            df.at[index, 'Status'] = 'Pending'

process_websites(websites, df)

# Print collected Facebook links and Gmail addresses
print(Panel.fit("\n".join(facebook_links), title="Facebook Links", border_style="bold blue", box=box.SQUARE))
print(Panel.fit("\n".join(gmail_addresses), title="Gmail Addresses", border_style="bold magenta", box=box.SQUARE))

# Print the count of successfully sent messages
print(Panel.fit(f"Successfully sent messages: {messages_sent}", border_style="bold green", box=box.SQUARE))

# After processing all websites, save the DataFrame back to a CSV file
df.to_csv('Updated Examplar Prospects List.csv', index=False)
