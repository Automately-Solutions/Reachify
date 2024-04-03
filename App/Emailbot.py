import pandas as pd
import requests
from bs4 import BeautifulSoup
import re
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Email setup
smtp_server = 'smtp.gmail.com'  # Your SMTP server
smtp_port = 443  # Your SMTP server's port
email_address = 'raoabdulhadi952@gmail.com'  # Your email
email_password = '--'  # Your email password or app-specific password

# Email content
subject = 'My MILLION DOLLAR offer to you'
body = """
I've been impressed by your service quality and the audience you've attracted. Here's an offer for you: At WordSmith, we deliver expert product design and graphic services, and here's the twist - you don’t pay a cent until you see satisfactory results. It’s all about elevating your brand's visual identity with the summer demand surges, risk-free.

Would you be open to exploring this unique opportunity to enhance your visuals without upfront costs?

Best,

- WordSmith
"""

def send_email(recipient_email):
    message = MIMEMultipart()
    message['From'] = email_address
    message['To'] = recipient_email
    message['Subject'] = subject
    message.attach(MIMEText(body, 'plain'))
    text = message.as_string()
    
    with smtplib.SMTP_SSL(smtp_server, smtp_port) as server:
        server.login(email_address, email_password)
        server.sendmail(email_address, recipient_email, text)

# Load the CSV file
df = pd.read_csv('Examplar Prospects List.csv')
websites = df.iloc[:, 5]  # Adjust based on your CSV structure
email_pattern = re.compile(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}")

for url in websites:
    try:
        response = requests.get(url, timeout=10)
        if 200 <= response.status_code < 300:
            soup = BeautifulSoup(response.text, 'html.parser')
            text = soup.get_text()
            emails = set(email_pattern.findall(text))  # Find unique emails
            
            for email in emails:
                print(f"Sending email to: {email}")
                send_email(email)
                print(f"Email sent to: {email}")
                
    except Exception as e:
        print(f"Failed to process {url}: {str(e)}")
