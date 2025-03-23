import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
from rich.console import Console
from rich.traceback import install
from rich.table import Table
from rich.panel import Panel

from Emailbot import send_email

# Enable rich traceback for debugging
install(show_locals=True)

# Initialize the console
console = Console()

# Constant sender email (used for all emails)
SENDER_EMAIL = "your_verified_email@example.com"

# Function to extract social media links and emails
def extract_social_links(url):
    try:
        response = requests.get(url, timeout=10)
        if response.status_code != 200:
            return None, None, None, None
        
        soup = BeautifulSoup(response.text, 'html.parser')

        instagram_link = None
        facebook_link = None
        gmail_address = None
        linkedin_link = None

        # Regex-based search in HTML text
        instagram_search = re.search(r'https?://(www\.)?instagram\.com/([a-zA-Z0-9_]+)', response.text)
        if instagram_search:
            instagram_link = instagram_search.group(0)

        facebook_search = re.search(r'https?://(www\.)?facebook\.com/([a-zA-Z0-9_\.]+)', response.text)
        if facebook_search:
            facebook_link = facebook_search.group(0)

        linkedin_search = re.search(r'https?://(www\.)?linkedin\.com/in/([a-zA-Z0-9-]+)', response.text)
        if linkedin_search:
            linkedin_link = linkedin_search.group(0)

        # Find visible Gmail addresses in the text
        gmail_search = re.search(r'([a-zA-Z0-9._%+-]+@gmail\.com)', response.text)
        if gmail_search:
            gmail_address = gmail_search.group(0)

        # Prioritize mailto: links for more accurate email detection
        mailto_links = soup.find_all('a', href=True)
        for link in mailto_links:
            href = link['href']
            if href.startswith('mailto:'):
                extracted_email = href.replace('mailto:', '').strip()
                if extracted_email.endswith('@gmail.com'):
                    gmail_address = extracted_email

        return instagram_link, facebook_link, gmail_address, linkedin_link

    except requests.exceptions.RequestException as e:
        console.print(f"[bold red]Error with URL {url}:[/bold red] {e}")
        return None, None, None, None

# Function to extract prospects and display social media links
def extract_prospects_with_links(file_name="Examplar Prospects List.csv"):
    df = pd.read_csv(file_name)
    df_selected = df.iloc[:, [0, 2]]  # Assuming Column A and C for 'Prospect Name' and 'Website'
    df_selected.columns = ["Prospect Name", "Website"]

    table = Table(title="Prospect Social Media and Website Info", show_lines=True)
    table.add_column("Prospect Name", style="bold cyan")
    table.add_column("Website", style="bold magenta")
    table.add_column("Instagram", style="bold green")
    table.add_column("Facebook", style="bold blue")
    table.add_column("Gmail", style="bold yellow")
    table.add_column("LinkedIn", style="bold red")

    for _, row in df_selected.iterrows():
        prospect_name = row["Prospect Name"]
        website = row["Website"]

        instagram, facebook, gmail, linkedin = extract_social_links(website)

        table.add_row(
            str(prospect_name), str(website), 
            str(instagram or "N/A"), 
            str(facebook or "N/A"), 
            str(gmail or "N/A"), 
            str(linkedin or "N/A")
        )

    console.print(table)

# Function to generate outreach messages and send emails
def generate_and_send_emails(file_name="Examplar Prospects List.csv"):
    df = pd.read_csv(file_name)
    df_selected = df.iloc[:, [0, 2]]  # Assuming columns 'Prospect Name' and 'Website'
    df_selected.columns = ["Prospect Name", "Website"]

    for _, row in df_selected.iterrows():
        prospect_name = row["Prospect Name"]
        website = row["Website"]

        # Extract contact info
        _, _, gmail, _ = extract_social_links(website)

        if not gmail:
            console.print(f"[bold yellow]Skipping {prospect_name} (No valid Gmail found)[/bold yellow]")
            continue

        # Generate personalized outreach message
        message = f"""Hey {prospect_name}, just came across your latest post and loved it and I believe I have the hack to solving your low traffic problem without the normal hassle. I have been impressed with the quality of your services yet I notice you struggling with:

— Finding new clients for your business  
— Improving the quality of the leads you get  
— Increasing your web traffic and profits  

I believe I can help you overcome these issues, and I am willing to do it for free to prove myself to you. If you are interested, you can reply “START” to this email and I will be in touch with you shortly.  

I have attached some of my previous work below the email to give you a sense of the quality of the designs you could expect from my side.  

Again, If you’re busy, I can understand.  

Rao, Chief Executive Officer  
Upkick Marketing Agency  
upkick.marketing [Instagram]  
wordsmithscript@gmail.com [Email]
        """

        # Display the message in a panel
        console.print(Panel(message, title=f"Outreach Message for {prospect_name}", expand=False, border_style="bold green"))

        # Send the email
        try:
            send_email(message, SENDER_EMAIL, gmail)
            console.print(f"[bold green]Email sent successfully to {prospect_name} ({gmail})[/bold green]")
        except Exception as e:
            console.print(f"[bold red]Failed to send email to {prospect_name} ({gmail}): {e}[/bold red]")

# Run the functions
extract_prospects_with_links()      # Display social media and Gmail addresses
generate_and_send_emails()          # Generate messages and send emails
