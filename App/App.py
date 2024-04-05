from rich import print
from rich.panel import Panel
from rich import box
import pandas as pd
import requests
from bs4 import BeautifulSoup
import re
from instagrapi import Client
from instagrapi.exceptions import UserNotFound, LoginRequired
import logging

# Setup logger
logger = logging.getLogger()

# Initialize the Instagrapi client
cl = Client()

# Define global variables for login credentials
USERNAME = "your_username"  # Replace with your Instagram username
PASSWORD = "your_password"  # Replace with your Instagram password

def login_user():
    """
    Attempts to login to Instagram using either the provided session information
    or the provided username and password.
    """
    session = cl.load_settings("session.json")

    login_via_session = False
    login_via_pw = False

    if session:
        try:
            cl.set_settings(session)
            cl.login(USERNAME, PASSWORD)
            try:
                cl.get_timeline_feed()
            except LoginRequired:
                logger.info("Session is invalid, need to login via username and password")
                old_session = cl.get_settings()
                cl.set_settings({})
                cl.set_uuids(old_session["uuids"])
                cl.login(USERNAME, PASSWORD)
            login_via_session = True
        except Exception as e:
            logger.info(f"Couldn't login user using session information: {e}")

    if not login_via_session:
        try:
            logger.info(f"Attempting to login via username and password. Username: {USERNAME}")
            if cl.login(USERNAME, PASSWORD):
                login_via_pw = True
        except Exception as e:
            logger.info(f"Couldn't login user using username and password: {e}")

    if not login_via_pw and not login_via_session:
        raise Exception("Couldn't login user with either password or session")

def scrape_links(websites, pattern):
    """
    Generic function to scrape links matching a given pattern from a list of websites.
    """
    matching_links = []
    for url in websites:
        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                links = soup.find_all('a', href=True)
                for link in links:
                    if re.search(pattern, link['href']):
                        matching_links.append(link['href'])
        except requests.RequestException:
            pass  # You might want to log errors or handle them differently
    return list(set(matching_links))  # Return unique links

def send_instagram_messages(websites):
    """
    Function to send Instagram messages to users found on the websites.
    """
    messages_sent = 0
    for url in websites:
        found_instagram = False
        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                links = soup.find_all('a', href=True)
                for link in links:
                    href = link['href']
                    if "instagram.com" in href:
                        username = re.search(r"instagram.com/([^/?#&]+)", href)
                        if username:
                            found_instagram = True
                            username = username.group(1)
                            try:
                                user_id = cl.user_id_from_username(username)
                                message = f"Hey {username},\n\nImpressed by the range of services, especially as summer heats up the demand. At Pixelevate, we offer expert digital marketing with a twist: no payment until you see results. Ready to make this summer your most profitable one? Let's chat."
                                cl.direct_send(message, [user_id])
                                print(Panel.fit(f"Message sent to {username}", border_style="bold green", box=box.SQUARE))
                                messages_sent += 1
                            except UserNotFound:
                                print(Panel.fit(f"Instagram user {username} not found.", border_style="bold yellow", box=box.SQUARE))
                            break
        except requests.RequestException:
            pass  # Handle errors as needed
    print(Panel.fit(f"Successfully sent messages: {messages_sent}", border_style="bold green", box=box.SQUARE))

# Call the login function at the start of your script
login_user()

# Example usage
file_path = 'Examplar Prospects List.csv'
df = pd.read_csv(file_path)
websites = df.iloc[:, 5]  # Adjust the column index as necessary

# Scrape Facebook links and Gmail addresses
facebook_links = scrape_links(websites, r"facebook.com")
gmail_addresses = scrape_links(websites, r"\b[A-Za-z0-9._%+-]+@gmail.com\b")

# Print Facebook links and Gmail addresses
print(Panel.fit("\n".join(facebook_links), title="Facebook Links", border_style="bold blue", box=box.SQUARE))
print(Panel.fit("\n".join(gmail_addresses), title="Gmail Addresses", border_style="bold magenta", box=box.SQUARE))

# Send Instagram messages
send_instagram_messages(websites)
