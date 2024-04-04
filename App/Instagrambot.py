from rich import box
from rich import text
from rich import print
from rich.panel import Panel

import pandas as pd
import requests
from bs4 import BeautifulSoup
import re
from instagrapi import Client

# Load the CSV file
file_path = 'Examplar Prospects List.csv'
df = pd.read_csv(file_path)

# Assuming the website links are in column 'F'
websites = df.iloc[:, 5]  # Adjust the column index as necessary

# Instagrapi client setup
cl = Client()
cl.login(username="username", password="password")

def extract_instagram_username(instagram_url):
    # This function assumes that the Instagram URL is in the form of https://www.instagram.com/username/
    # It extracts 'username' from the URL
    match = re.search(r"instagram.com/([^/?#&]+)", instagram_url)
    if match:
        return match.group(1)
    else:
        return None

for url in websites:
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
                        # Get user ID from username
                        user_id = cl.user_id_from_username(username)
                        # Send message
                        cl.direct_send("Hi, How are you", [user_id])
                        print(Panel.fit(f"Message sent to {username}", border_style="bold green", box = box.SQUARE))
        else:
            print(Panel.fit(f"Could not retrieve {url}", border_style="bold red", box = box.SQUARE))
    except requests.RequestException as e:
        print(Panel.fit(f"Error: {e}", border_style = "bold red"))
