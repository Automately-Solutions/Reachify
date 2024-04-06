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

# Load the .xlsx file using pandas
file_path = 'Examplar Prospects List.xlsx'
df = pd.read_excel(file_path)

# Assuming the website links are in column 'F'
websites = df.iloc[:, 5]  # Adjust the column index as necessary

# Instagrapi client setup with proxy
cl = Client()
before_ip = cl._send_public_request("https://api.ipify.org/")
# Replace "<api_key>" with your actual API key for the proxy service
cl.set_proxy("http://<api_key>@proxy.soax.com:9137")
after_ip = cl._send_public_request("https://api.ipify.org/")

cl.delay_range = [1, 3]  # Set delay range for requests

# Replace these with your actual username and password
USERNAME = "instagram_username"
PASSWORD = "instagram_password"

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

def send_instagram_message(websites, df):
    for index, url in websites.iteritems():
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
                                message = f"Hey {username},\n\nImpressed by the range of services, especially as summer heats up the demand. At Pixelevate, we offer expert digital marketing with a twist: no payment until you see results. Ready to make this summer your most profitable one? Let's chat."
                                cl.direct_send(message, [user_id])
                                df.at[index, 'Status'] = 'Done'  # Update the status in the DataFrame
                                print(Panel.fit(f"Message sent to {username}", border_style="bold green", box=box.SQUARE))
                                break
                            except exceptions.UserNotFound:
                                print(Panel.fit(f"Instagram user {username} not found. Skipping...", border_style="bold yellow", box=box.SQUARE))
                                df.at[index, 'Status'] = 'Pending'
            else:
                print(Panel.fit(f"Could not retrieve {url}", border_style="bold red", box=box.SQUARE))
                df.at[index, 'Status'] = 'Pending'
        except requests.RequestException as e:
            print(Panel.fit(f"Error: {e}", border_style="bold red", box=box.SQUARE))
            df.at[index, 'Status'] = 'Pending'

# Call the function and pass the DataFrame as an argument
send_instagram_message(websites, df)

# After processing all websites, save the DataFrame back to an .xlsx file
df.to_excel('Updated Examplar Prospects List.xlsx', index=False)
