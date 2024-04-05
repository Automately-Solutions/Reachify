from rich import print
from rich.panel import Panel
from rich import box
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
    """Extract Instagram username from URL."""
    match = re.search(r"instagram.com/([^/?#&]+)", instagram_url)
    if match:
        return match.group(1)
    else:
        return None

def scrape_facebook_links(websites):
    """Scrape Facebook links from a list of websites."""
    facebook_links = []
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
        except Exception as e:
            print(Panel.fit(f"Error retrieving {url}: {e}", border_style="bold red", box=box.SQUARE))
    return facebook_links

def scrape_gmail_addresses(websites):
    """Scrape Gmail addresses from a list of websites."""
    gmail_addresses = []
    for url in websites:
        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                emails = re.findall(r"[a-zA-Z0-9+_.-]+@gmail\.com", response.text)
                gmail_addresses.extend(emails)
        except Exception as e:
            print(Panel.fit(f"Error retrieving {url}: {e}", border_style="bold red", box=box.SQUARE))
    return list(set(gmail_addresses))  # Remove duplicates

def send_instagram_messages(websites, cl):
    """Send Instagram messages based on found Instagram profiles."""
    messages_sent = 0
    for url in websites:
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
                            try:
                                user_id = cl.user_id_from_username(username)
                                message = f"Hey {username}, \n\nImpressed by the range of services, especially as summer heats up the demand. At Pixelevate, we offer expert digital marketing with a twist: no payment until you see results. Ready to make this summer your most profitable one? Let's chat."
                                cl.direct_send(message, [user_id])
                                messages_sent += 1
                                break  # Stop checking further links once an Instagram username is found
                            except UserNotFound:
                                continue
        except requests.RequestException as e:
            print(Panel.fit(f"Error: {e}", border_style="bold red", box = box.SQUARE))
    return messages_sent

# Main Routine
facebook_links = scrape_facebook_links(websites)
print(Panel.fit(f"Facebook Links: {facebook_links}", border_style="bold green", box=box.SQUARE))

gmail_addresses = scrape_gmail_addresses(websites)
print(Panel.fit(f"Gmail Addresses: {gmail_addresses}", border_style="bold green", box=box.SQUARE))

messages_sent = send_instagram_messages(websites, cl)
print(Panel.fit(f"Successfully sent messages: {messages_sent}", border_style="bold green", box=box.SQUARE))
