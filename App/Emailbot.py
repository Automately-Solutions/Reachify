from bs4 import BeautifulSoup
import requests
import re  # For regex
from mailjet_rest import Client
import csv  # For CSV file handling
from rich import print, text, box
from rich.panel import Panel
import sys  # For exiting the script

# Mailjet setup
api_key = ''
api_secret = ''
mailjet = Client(auth=(api_key, api_secret), version='v3.1')

# Function to scrape the website for an email address
def scrape_website_for_email(url):
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            text = soup.get_text()
            # Updated regex to capture more general email addresses
            email_addresses = re.findall(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+", text)
            if email_addresses:
                return email_addresses[0]  # Return the first found email address
            else:
                print(Panel.fit(f"No email addresses found on {url}.", border_style="bold red", box=box.SQUARE))
                return None
    except requests.RequestException as e:
        print(Panel.fit(f"Failed to access {url}: {e}", border_style="bold red", box=box.SQUARE))
        return None

# Function to send an email using Mailjet to a specified email address
def send_email(recipient_email):
    if recipient_email is None:
        print(Panel.fit("No recipient email provided.", border_style="bold red", box=box.SQUARE))
        return
    
    data = {
      'Messages': [
        {
          "From": {
            "Email": "wordsmithscript@gmail.com",
            "Name": "WordSmith Corp."
          },
          "To": [
            {
              "Email": recipient_email,
              "Name": recipient_email,
            }
          ],
          "Subject": "My MILLION DOLLAR offer to you.",
          "TextPart": "I have been impressed by your service quality and the audience you've attracted. Here is an offer for you...",
          "HTMLPart": "<h3>This is your chance at a lifetime opportunity, with zero expenses!</h3><br>I wish you a happy summer!",
          "CustomID": "AppGettingStartedTest"
        }
      ]
    }
    result = mailjet.send.create(data=data)
    print(Panel.fit(f"Email sent to {recipient_email}: {result.status_code}", border_style="bold green", box=box.SQUARE))
    print(result.json())

# Read URLs from CSV and execute
def process_urls_from_csv(csv_file_path):
    with open(csv_file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  # Skip the header row
        for row in reader:
            # Check for user input to quit
            print("Press 'q' and Enter to quit, or just Enter to continue: ")
            choice = input()
            if choice.strip().lower() == 'q':
                print("Quitting...")
                sys.exit(0)  # Exit the script
            
            website_url = row[5]  # Assuming 'F' column is the 6th column
            print(Panel.fit(f"Processing website: {website_url}", border_style="bold yellow", box=box.SQUARE))
            scraped_email = scrape_website_for_email(website_url)
            
            if scraped_email:
                print(Panel.fit(f"Sending email to {scraped_email}...", border_style="bold yellow", box=box.SQUARE))
                send_email(scraped_email)
            else:
                print(Panel.fit(f"No valid email found for {website_url}.", border_style="bold red", box=box.SQUARE))

# Main execution
if __name__ == "__main__":
    csv_file_path = "Examplar Prospects List.csv"  # Replace with your actual CSV file path
    process_urls_from_csv(csv_file_path)
