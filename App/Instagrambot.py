from instagrapi import Client
import random

# Instagrapi Client initialization with your Instagram account credentials
cl = Client()
cl.login("wordsmith.agency", "wordsmithscriptsforyou")

# Assuming you have a list of Instagram usernames previously collected
instagram_usernames = ['m3l4t0n', 'ricardozilla', 'thevituousone']  # Replace these with actual usernames

# Selecting one random username from the list
if instagram_usernames:
    selected_username = random.choice(instagram_usernames)
    user_id = cl.user_id_from_username(selected_username)
    cl.direct_send("Hi, How are you", [user_id])
    print(f"Message sent to {selected_username}")
else:
    print("No Instagram usernames available to message.")
