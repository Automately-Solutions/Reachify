from rich import text
from rich import box
from rich import print
from rich.panel import Panel

import pandas as pd
import requests
from bs4 import BeautifulSoup
import re
from instagrapi import Client
from instagrapi.exceptions import UserNotFound

# Load the CSV file
file_path = 'Examplar Prospects List.csv'
df = pd.read_csv(file_path)

# Assuming the website links are in column 'F'
websites = df.iloc[:, 5]  # Adjust the column index as necessary

# Instagrapi client setup
cl = Client()
cl.login(username="username", password="password")

def extract_instagram_username(instagram_url):
    match = re.search(r"instagram.com/([^/?#&]+)", instagram_url)
    if match:
        return match.group(1)
    else:
        return None

messages_sent = 0  # Initialize counter for successfully sent messages

for url in websites:
    found_instagram = False
    print(f"Checking {url}...")
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
                        found_instagram = True  # Instagram link found
                        try:
                            # Attempt to get user ID from username
                            user_id = cl.user_id_from_username(username)
                            # Prepare the personalized message
                            message = f"Hey {username},\n\nImpressed by the range of services, especially as summer heats up the demand. At Pixelevate, we offer expert digital marketing with a twist: no payment until you see results. Ready to make this summer your most profitable one? Let's chat."
                            # Send message
                            cl.direct_send(message, [user_id])
                            print(Panel.fit(f"Message sent to {username}", border_style="bold green", box=box.SQUARE))
                            messages_sent += 1
                        except UserNotFound:
                            print(Panel.fit(f"Instagram user {username} not found. Skipping...", border_style="bold yellow", box=box.SQUARE))
                        break  # Stop checking further links once an Instagram username is found
                        
            if not found_instagram:
                print(Panel.fit(f"No Instagram link found on {url}. Skipping...", border_style="bold yellow", box=box.SQUARE))
        else:
            print(Panel.fit(f"Could not retrieve {url}", border_style="bold red", box=box.SQUARE))
    except requests.RequestException as e:
        print(Panel.fit(f"Error: {e}", border_style="bold red"))

# Print the count of successfully sent messages
print(Panel.fit(f"Successfully sent messages: {messages_sent}", border_style="bold green", box=box.SQUARE))
