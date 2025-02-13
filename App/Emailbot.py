from rich import text
from rich import box
from rich import print
from rich.panel import Panel
from rich.traceback import install
install(show_locals=True)

import pandas as pd
import requests
import re
from bs4 import BeautifulSoup
import logging
from mailjet_rest import Client as MailjetClient
import time


# Load the CSV file
file_path = open("/Documents/Development/Reachify/App/Examplar Prospects List.csv")
df = pd.read_csv(file_path)

# Assuming the website links are in column 'C'
websites = df.iloc[:, 2]  # Adjust the column index as necessary

# Setup logging
logger = logging.getLogger()

# Mailjet setup
mailjet_api_key = 'MAILJET_API_KEY'
mailjet_api_secret = 'MAILJET_SECRET_KET'
mailjet_client = MailjetClient(auth=(mailjet_api_key, mailjet_api_secret), version='v3.1')

def send_email(recipient_email):
    data = {
      'Messages': [
        {
          "From": {
            "Email": "wordsmithscripts@gmail.com",
            "Name": "WordSmith Corp."
          },
          "To": [
            {
              "Email": recipient_email,
              "Name": "Dear Valued Customer"
            }
          ],
          "Subject": "Loved your last post",
          "TextPart": """I just came across your latest post and loved it, but I have the hack to solve your low traffic problem without the normal hassle. I have been impressed with the quality of your services yet I notice you struggling with :

                        — Finding new clients for your business
                        — Improving the quality of leads you get
                        — Increasing your web traffic and profits
                        
                        I believe I can help you overcome these issues, and I am willing to do it for free to prove myself to you. If you are interested, you can reply “START” to this email and I will be in-touch with you shortly.
                        
                        I have attached some of my previous work below the email to give you a sense of quality of the designs you could expect from my side.
                        
                        Again, If you’re busy, I can understand.
                        
                        Rao, Chief Executive Officer
                        Upkick Marketing Agency
                        upkick.marketing [Instagram]
                        wordsmithscript@gmail.com [Email]""",
          "CustomID": "OutreachTestingRuns"
        }
      ]
    }
    result = mailjet_client.send.create(data=data)
    if result.status_code == 200:
        print(Panel.fit(f"Email successfully sent to {recipient_email}", border_style="bold green", box=box.SQUARE))
    else:
        print(Panel.fit(f"Failed to send email to {recipient_email}. Error: {result.json()}", border_style="bold red", box=box.SQUARE))

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
    print(Panel.fit("\n".join(gmail_addresses), title="Gmail Addresses", border_style="bold red", box=box.SQUARE))

    # Email sending to the scraped Gmail addresses
    for email in gmail_addresses:
        send_email(email)

scrape_facebook_and_gmail(websites)