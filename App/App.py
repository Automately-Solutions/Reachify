import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
from rich.console import Console
from rich.traceback import install
from rich.table import Table
from rich.panel import Panel

from Emailbot import send_email
from Instagrambot import send_instagram_dm

# Enable rich traceback for debugging
install(show_locals=True)

# Initialize the console
console = Console()

# Constant sender email (used for all emails)
SENDER_EMAIL = "wordsmithscript@gmail.com"

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

        mailto_links = soup.find_all('a', href=True)
        for link in mailto_links:
            href = link['href']
            if href.startswith('mailto:'):
                gmail_address = href.replace('mailto:', '').strip()
                break
            
        if not gmail_address:
            email_search = re.search(r'[\w\.-]+@[\w\.-]+\.\w+', response.text)
            if email_search:
                raw_email = email_search.group(0)
                # Clean email from any leading/trailing non-email characters
                cleaned_email = re.sub(r'[^a-zA-Z0-9._%+-@]', '', raw_email)
                if re.fullmatch(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', cleaned_email):
                    gmail_address = cleaned_email


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
    table.add_column("Instagram", style="bold magenta")
    table.add_column("Facebook", style="bold blue")
    table.add_column("Gmail", style="bold green")
    table.add_column("LinkedIn", style="bold blue")

    for _, row in df_selected.iterrows():
        prospect_name = row["Prospect Name"]
        website = row["Website"]

        instagram, facebook, gmail, linkedin = extract_social_links(website)

        table.add_row(
            str(prospect_name),
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

    sent_emails = []  # List of successful email addresses
    failed_emails = []  # List of failed email addresses

    for _, row in df_selected.iterrows():
        prospect_name = row["Prospect Name"]
        website = row["Website"]

        # Extract contact info
        _, _, email, _ = extract_social_links(website)

        if not email:
            console.print(f"[bold yellow]Skipping {prospect_name} (No valid email found)[/bold yellow]")
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
            send_email(message, SENDER_EMAIL, email)
            console.print(f"[bold green]Email sent successfully to {prospect_name} ({email})[/bold green]")
            sent_emails.append(email)
        except Exception as e:
            console.print(f"[bold red]Failed to send email to {prospect_name} ({email}): {e}[/bold red]")
            failed_emails.append(email)

    # Print summary
    console.print(f"\n[bold cyan]Summary:[/bold cyan]")
    console.print(f"✅ Successfully sent {len(sent_emails)} emails:")
    for email in sent_emails:
        console.print(f"   - {email}")

    console.print(f"❌ Failed to send {len(failed_emails)} emails:")
    for email in failed_emails:
        console.print(f"   - {email}")

def generate_and_send_instagram_dms(file_name="Examplar Prospects List.csv"):
    """Extracts Instagram links from websites and sends DMs using send_instagram_dm()."""
    df = pd.read_csv(file_name)
    df_selected = df.iloc[:, [0, 2]]  # Assuming columns 'Prospect Name' and 'Website'
    df_selected.columns = ["Prospect Name", "Website"]

    sent_dms = []  # List of successful DMs
    failed_dms = []  # List of failed DMs

    for _, row in df_selected.iterrows():
        prospect_name = row["Prospect Name"]
        website = row["Website"]

        # Extract Instagram link
        instagram_link, _, _, _ = extract_social_links(website)

        if not instagram_link:
            console.print(f"[bold yellow]Skipping {prospect_name} (No Instagram found)[/bold yellow]")
            continue

        # Send the DM
        success = send_instagram_dm(instagram_link, prospect_name)
        if success:
            sent_dms.append(prospect_name)
        else:
            failed_dms.append(prospect_name)

    # Print summary
    console.print(f"\n[bold cyan]Summary:[/bold cyan]")
    console.print(f"✅ Successfully sent {len(sent_dms)} DMs:")
    for name in sent_dms:
        console.print(f"   - {name}")

    console.print(f"❌ Failed to send {len(failed_dms)} DMs:")
    for name in failed_dms:
        console.print(f"   - {name}")



# extract_prospects_with_links()
# generate_and_send_emails()
generate_and_send_instagram_dms()
