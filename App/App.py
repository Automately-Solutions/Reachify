import pandas as pd
import requests
from bs4 import BeautifulSoup
import re
from rich import print
from rich.panel import Panel
from rich import box
from rich import text

# Load the CSV file
file_path = 'Examplar Prospects List.csv'
df = pd.read_csv(file_path)

# Assuming the website links are in column 'F'
websites = df.iloc[:, 5]  # Adjust the column index as necessary

# Regular expression pattern for matching email addresses
email_pattern = re.compile(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}")

for url in websites:
    print(f"Checking {url}...")
    social_media_links = []
    emails = []
    try:
        response = requests.get(url, timeout=10)
        if 200 <= response.status_code < 300:
            status = 'Online'

            # Parse the HTML content
            soup = BeautifulSoup(response.text, 'html.parser')
            links = soup.find_all('a', href=True)
            
            # Search for Instagram and Facebook links
            for link in links:
                href = link['href']
                if "instagram.com" in href or "facebook.com" in href:
                    social_media_links.append(href)

            # Search for email addresses
            text = soup.get_text()
            emails = email_pattern.findall(text)
            emails = list(set(emails))  # Remove duplicates

            # Prepare the content for the panel
            content_lines = [f"URL: {url}", f"Status: {status}"]
            if social_media_links:
                content_lines.append("Social Media Links:")
                content_lines.extend(social_media_links)
            else:
                content_lines.append("[b red]No social media links found.[/]")
                
            if emails:
                content_lines.append("Email Addresses:")
                content_lines.extend(emails)
            else:
                content_lines.append("[b red]No email addresses found.[/]")

            # Join the content lines and print the panel
            panel_content = "\n".join(content_lines)
            print(Panel.fit(panel_content, border_style="bold green", box = box.SQUARE))

        else:
            status = 'Offline or Error'
            print(Panel.fit(f"URL: {url}\nStatus: {status}", border_style="bold red", box = box.SQUARE))

    except requests.RequestException:
        status = 'Offline or Error'
        print(Panel.fit(f"URL: {url}\nStatus: {status}", border_style="bold red", box = box.SQUARE))
