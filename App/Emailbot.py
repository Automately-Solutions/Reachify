import pandas as pd
import requests
from bs4 import BeautifulSoup
import re
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from rich.panel import Panel
from rich import box
from rich import print
from rich.traceback import install
install(show_locals=True)

# Update these with your actual details
SMTP_SERVER = "in-v3.mailjet.com"
SMTP_PORT = 587
SMTP_USER = 'mailjet_api_key'
SMTP_PASSWORD = 'mailjet_secret_key'
FROM_EMAIL = 'wordsmithscript@gmail.com'
SUBJECT = 'Test Email from Script'
EMAIL_BODY = 'This is a test email sent from the Python script.'

# Load CSV
df = pd.read_csv('test_websites.csv')

# Initialize variables
email_addresses = []

def scrape_emails(url):
    """Scrape email addresses from the given URL."""
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            text = soup.get_text()
            emails = re.findall(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+", text)
            email_addresses.extend(emails)
            print(f"Found emails: {emails} in {url}")
        else:
            print(Panel.fit(f"Failed to access {url}", box=box.SQUARE, border_style="bold red"))
    except requests.RequestException as e:
        print(Panel.fit(f"Request failed: {e}", border_style="bold red", box=box.SQUARE))

def send_email(recipient_email):
    """Send an email to the specified recipient."""
    msg = MIMEMultipart()
    msg['From'] = FROM_EMAIL
    msg['To'] = recipient_email
    msg['Subject'] = SUBJECT
    msg.attach(MIMEText(EMAIL_BODY, 'plain'))
    try:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(SMTP_USER, SMTP_PASSWORD)
        server.send_message(msg)
        print(Panel.fit(f"Email sent to {recipient_email}", border_style="bold green", box=box.SQUARE))
    except Exception as e:
        print(f"Failed to send email to {recipient_email}: {e}")
    finally:
        server.quit()

# Process each website in the CSV
for _, row in df.iterrows():
    scrape_emails(row['Website'])

# Assuming you want to send an email to the first found address for testing
if email_addresses:
    send_email(email_addresses[0])
else:
    print("No email addresses found.")
