from bs4 import BeautifulSoup
import requests
from mailjet_rest import Client
import os

# Mailjet setup
api_key = 'your_mailjet_api_key'
api_secret = 'your_mailjet_api_secret'
mailjet = Client(auth=(api_key, api_secret), version='v3.1')

# Define the single website URL for testing
website_url = "https://example.com"  # Replace with the website you want to test

# Function to scrape the website
def scrape_website(url):
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            # Example: print all 'a' tags to demonstrate scraping
            # Modify as needed to extract specific links or information
            for link in soup.find_all('a', href=True):
                print(link.get('href'))
    except requests.RequestException as e:
        print(f"Failed to access {url}: {e}")

# Function to send an email using Mailjet
def send_email():
    data = {
      'Messages': [
        {
          "From": {
            "Email": "sender_email@example.com",
            "Name": "Sender Name"
          },
          "To": [
            {
              "Email": "recipient_email@example.com",
              "Name": "Recipient Name"
            }
          ],
          "Subject": "Greetings from Mailjet.",
          "TextPart": "My first Mailjet email",
          "HTMLPart": "<h3>Dear passenger 1, welcome to <a href='https://www.mailjet.com/'>Mailjet</a>!</h3><br />May the delivery force be with you!",
          "CustomID": "AppGettingStartedTest"
        }
      ]
    }
    result = mailjet.send.create(data=data)
    print(result.status_code)
    print(result.json())

# Main execution
if __name__ == "__main__":
    print(f"Scraping website: {website_url}")
    scrape_website(website_url)
    
    print("Sending test email with Mailjet...")
    send_email()
