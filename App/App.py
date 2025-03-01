import requests
from bs4 import BeautifulSoup
import re
from rich.table import Table
from rich.console import Console
from rich.traceback import install
import pandas as pd

# Enable rich traceback for better debugging
install(show_locals=True)

# Initialize the console for rich printing
console = Console()

# Function to extract social media links and emails
def extract_social_links(url):
    try:
        # Send a request to get the HTML content of the webpage
        response = requests.get(url)
        if response.status_code != 200:
            return None, None, None, None
        
        # Parse the HTML content with BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Search for Instagram, Facebook, Gmail, and LinkedIn links using regex
        instagram_link = None
        facebook_link = None
        gmail_address = None
        linkedin_link = None

        # Instagram: Matches 'www.instagram.com/username'
        instagram_search = re.search(r'https?://(www\.)?instagram\.com/([a-zA-Z0-9_]+)', response.text)
        if instagram_search:
            instagram_link = instagram_search.group(0)

        # Facebook: Matches 'www.facebook.com/username'
        facebook_search = re.search(r'https?://(www\.)?facebook\.com/([a-zA-Z0-9_\.]+)', response.text)
        if facebook_search:
            facebook_link = facebook_search.group(0)

        # Gmail: Matches 'mailto:someone@gmail.com'
        gmail_search = re.search(r'([a-zA-Z0-9._%+-]+@gmail\.com)', response.text)
        if gmail_search:
            gmail_address = gmail_search.group(0)

        # LinkedIn: Matches 'www.linkedin.com/in/username'
        linkedin_search = re.search(r'https?://(www\.)?linkedin\.com/in/([a-zA-Z0-9-]+)', response.text)
        if linkedin_search:
            linkedin_link = linkedin_search.group(0)

        return instagram_link, facebook_link, gmail_address, linkedin_link

    except requests.exceptions.RequestException as e:
        print(f"Error with URL {url}: {e}")
        return None, None, None, None

# Function to extract prospects and social media links
def extract_prospects_with_links(file_name="Examplar Prospects List.csv"):
    # Read the CSV file
    df = pd.read_csv(file_name)
    df_selected = df.iloc[:, [0, 2]]  # Assuming Column A and C for 'Prospect Name' and 'Website'
    df_selected.columns = ["Prospect Name", "Website"]

    # Initialize a table for displaying results
    table = Table(title="Prospect Social Media and Website Info", show_lines=True)
    table.add_column("Prospect Name", style="bold cyan")
    table.add_column("Website", style="bold magenta")
    table.add_column("Instagram", style="bold green")
    table.add_column("Facebook", style="bold blue")
    table.add_column("Gmail", style="bold yellow")
    table.add_column("LinkedIn", style="bold red")

    # Loop over each prospect and extract social media links
    for _, row in df_selected.iterrows():
        prospect_name = row["Prospect Name"]
        website = row["Website"]

        # Extract social media links from the website
        instagram, facebook, gmail, linkedin = extract_social_links(website)

        # Add row to the table (ensure all values are strings or "N/A" for None values)
        table.add_row(str(prospect_name), str(website), 
                      str(instagram or "N/A"), 
                      str(facebook or "N/A"), 
                      str(gmail or "N/A"), 
                      str(linkedin or "N/A"))

    # Print the table
    console.print(table)

# Call the function to extract and display the data
extract_prospects_with_links()
