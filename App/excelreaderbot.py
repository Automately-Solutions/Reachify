import pandas as pd
import requests
from bs4 import BeautifulSoup
from rich import print
from rich.panel import Panel

# Load the CSV file
file_path = 'Examplar Prospects List.csv'
df = pd.read_csv(file_path)

# Assuming the website links are in column 'F'
websites = df.iloc[:, 5]  # Adjust the column index as necessary

# Initialize a list to store the status of each website and social media links
status_list = []
social_media_links = []

for url in websites:
    print(f"Checking {url}...")
    try:
        response = requests.get(url, timeout=10)
        if 200 <= response.status_code < 300:
            status = 'Online'
            print(Panel.fit(f"URL: {url}\nStatus: {status}", border_style="bold green"))

            # Parse the HTML content
            soup = BeautifulSoup(response.text, 'html.parser')
            links = soup.find_all('a', href=True)
            
            # Initialize a list to store found social media links for the current website
            found_links = []

            # Search for Instagram and Facebook links
            for link in links:
                href = link['href']
                if "instagram.com" in href or "facebook.com" in href:
                    found_links.append(href)

            if found_links:
                print(f"Found social media links for {url}: {found_links}")
                social_media_links.append(found_links)
            else:
                print(f"No social media links found for {url}.")
                social_media_links.append("None")
        else:
            status = 'Offline or Error'
            print(Panel.fit(f"URL: {url}\nStatus: {status}", border_style="bold red"))
            social_media_links.append("None")
    except requests.RequestException:
        status = 'Offline or Error'
        print(Panel.fit(f"URL: {url}\nStatus: {status}", border_style="bold red"))
        social_media_links.append("None")
    
    status_list.append(status)

# Add the status and found social media links back to the dataframe
df['Website Status'] = status_list
df['Social Media Links'] = social_media_links
df.to_csv('website_status_and_social_media_links.csv', index=False)
3