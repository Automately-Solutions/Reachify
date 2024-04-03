import pandas as pd
import requests
from bs4 import BeautifulSoup
import re
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from rich import print, box
from rich.panel import Panel

# Load the CSV file
file_path = 'Examplar Prospects List.csv'
df = pd.read_csv(file_path)

# Assuming the website links are in column 'F'
websites = df.iloc[:, 5]  # Adjust the column index as necessary

# Regular expression pattern for matching email addresses
email_pattern = re.compile(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}")

def send_email_via_twilio_sendgrid(to_email, subject, html_content):
    # Setup the email parameters
    from_email = 'from_email@example.com'  # Replace this with your verified Twilio SendGrid sender email
    message = Mail(
        from_email=from_email,
        to_emails=to_email,
        subject=subject,
        html_content=html_content
    )
    try:
        # Send the email
        sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
        response = sg.send(message)
        print(f"Email successfully sent to: {to_email}")
    except Exception as e:
        print(f"Failed to send email to {to_email}: {str(e)}")

# Email subject and content
email_subject = "My MILLION DOLLAR offer to you"
email_content = """
<strong>I've been impressed by your service quality and the audience you've attracted.</strong> Here's an offer for you: At WordSmith, we deliver expert product design and graphic services, and here's the twist - you don’t pay a cent until you see satisfactory results. It’s all about elevating your brand's visual identity with the summer demand surges, risk-free.<br><br>

Would you be open to exploring this unique opportunity to enhance your visuals without upfront costs?<br><br>

Best,<br>
- WordSmith
"""

for url in websites:
    print(f"Checking {url}...")
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            text = soup.get_text()
            emails = set(email_pattern.findall(text))
            
            for email in emails:
                send_email_via_twilio_sendgrid(email, email_subject, email_content)
            
            print(Panel.fit(f"Processed {url}", border_style="bold green", box=box.SQUARE))
        else:
            print(Panel.fit(f"URL: {url}\nStatus: Error or Offline", border_style="bold red", box=box.SQUARE))
    except requests.RequestException:
        print(Panel.fit(f"URL: {url}\nStatus: Error or Offline", border_style="bold red", box=box.SQUARE))