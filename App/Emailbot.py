from bs4 import BeautifulSoup
import requests
import re  # For regex
from mailjet_rest import Client
import csv  # For CSV file handling

# Mailjet setup
api_key = '372eefae66841cfce3f97b7ddcc5473a'
api_secret = '-'
mailjet = Client(auth=(api_key, api_secret), version='v3.1')

# Function to scrape the website for a Gmail address
def scrape_website_for_gmail(url):
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            text = soup.get_text()
            gmail_addresses = re.findall(r"[a-zA-Z0-9_.+-]+@gmail.com", text)
            if gmail_addresses:
                return gmail_addresses[0]  # Return the first found Gmail address
            else:
                print(f"No Gmail addresses found on {url}.")
                return None
    except requests.RequestException as e:
        print(f"Failed to access {url}: {e}")
        return None

# Function to send an email using Mailjet to a specified email address
def send_email(recipient_email):
    if recipient_email is None:
        print("No recipient email provided.")
        return
    
    data = {
      'Messages': [
        {
          "From": {
            "Email": "wordsmithscript@gmail.com",
            "Name": "Sender Name"
          },
          "To": [
            {
              "Email": recipient_email,
              "Name": "Recipient Name"
            }
          ],
          "Subject": "Greetings from Mailjet.",
          "TextPart": "This is a test email sent using Mailjet.",
          "HTMLPart": "<h3>Dear recipient, welcome to Mailjet!</h3><br>May the delivery force be with you!",
          "CustomID": "AppGettingStartedTest"
        }
      ]
    }
    result = mailjet.send.create(data=data)
    print(f"Email sent to {recipient_email}: {result.status_code}")
    print(result.json())

# Read URLs from CSV and execute
def process_urls_from_csv(csv_file_path):
    with open(csv_file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  # Skip the header row
        for row in reader:
            website_url = row[5]  # Assuming 'F' column is the 6th column (0-indexed)
            print(f"Processing website: {website_url}")
            scraped_email = scrape_website_for_gmail(website_url)
            
            if scraped_email:
                print(f"Sending email to {scraped_email}...")
                send_email(scraped_email)
            else:
                print(f"No valid email found for {website_url}.")

# Main execution
if __name__ == "__main__":
    csv_file_path = "websites.csv"  # Replace with your CSV file path
    process_urls_from_csv(csv_file_path)
