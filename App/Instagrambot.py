from instagrapi import Client
from instagrapi.exceptions import UserNotFound
from rich.console import Console
import re

console = Console()

# Initialize and login to Instagram
cl = Client()
cl.login(username="username", password="password")

def send_instagram_dm(instagram_url, business_name):
    """Sends a DM to the given Instagram profile URL with a personalized message."""
    username = extract_instagram_username(instagram_url)
    if not username:
        print(f"[bold yellow]Invalid Instagram URL: {instagram_url}[/bold yellow]")
        return False
    
    try:
        user_id = cl.user_id_from_username(username)
        message = f"Hey {business_name},\n\nImpressed by the range of services, especially as summer heats up the demand. At Pixelevate, we offer expert digital marketing with a twist: no payment until you see results. Ready to make this summer your most profitable one? Let's chat."
        cl.direct_send(message, [user_id])
        console.print(f"[bold green]Message sent to {business_name} ({username})[/bold green]")
        return True
    except UserNotFound:
        console.print(f"[bold yellow]Instagram user {username} not found. Skipping...[/bold yellow]")
        return False

def extract_instagram_username(instagram_url):
    """Extracts the username from an Instagram URL."""
    match = re.search(r"instagram.com/([^/?#&]+)", instagram_url)
    return match.group(1) if match else None

def get_instagram_post_stats(post_url_or_code):

    try:
        # Determine if input is URL or shortcode
        if "instagram.com/p/" in post_url_or_code:
            media_pk = cl.media_pk_from_url(post_url_or_code)
        else:
            media_pk = cl.media_pk_from_code(post_url_or_code)

        media_info = cl.media_info(media_pk)
        like_count = media_info.like_count
        view_count = media_info.view_count

        return {
            "like_count": like_count,
            "view_count": view_count
        }

    except Exception as e:
        print(f"Error fetching stats: {e}")
        return None

stats = get_instagram_post_stats("https://www.instagram.com/p/DIEw5uLIKeD/")
print(stats)