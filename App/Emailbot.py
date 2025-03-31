import os
from mailjet_rest import Client

# Mailjet API Constants (replace with your actual API keys)
MJ_APIKEY_PUBLIC = "API"
MJ_APIKEY_PRIVATE = "SECRET"

# Initialize the Mailjet client
mailjet = Client(auth=(MJ_APIKEY_PUBLIC, MJ_APIKEY_PRIVATE), version='v3.1')

def send_email(message, sender_email, receiver_email):
    """Sends an email using the Mailjet API.

    Parameters:
    - message (str): The email body content.
    - sender_email (str): The email address of the sender.
    - receiver_email (str): The email address of the recipient.
    """

    # Prepare email payload
    data = {
        'Messages': [
            {
                "From": {
                    "Email": sender_email,
                    "Name": "Your Name"
                },
                "To": [
                    {
                        "Email": receiver_email,
                        "Name": "Recipient"
                    }
                ],
                "Subject": "Exclusive Opportunity!",
                "TextPart": message,
                "HTMLPart": f"<p>{message.replace('\n', '<br>')}</p>"
            }
        ]
    }

    # Send the email
    try:
        result = mailjet.send.create(data=data)
        print(f"Email sent to {receiver_email}: Status {result.status_code}")
        print(result.json())
    except Exception as e:
        print(f"Error sending email to {receiver_email}: {e}")
