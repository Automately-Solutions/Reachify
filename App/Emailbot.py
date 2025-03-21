import os
import pandas as pd
from mailjet_rest import Client

# Load API credentials from environment variables
api_key = os.environ.get('MJ_APIKEY_PUBLIC')
api_secret = os.environ.get('MJ_APIKEY_PRIVATE')

# Initialize Mailjet Client
mailjet = Client(auth=(api_key, api_secret), version='v3.1')

# Read the master CSV file containing outreach messages
def load_email_data(file_name="Examplar Prospects List.csv"):
    df = pd.read_csv(file_name)
    df_selected = df.iloc[:, [0, 1, 3]]  # Assuming Name, Email, and Outreach Message
    df_selected.columns = ["Prospect Name", "Email", "Message"]
    return df_selected

# Function to send emails
def send_emails(file_name="Examplar Prospects List.csv", sender_email="your_email@example.com", sender_name="Your Name"):
    df = load_email_data(file_name)

    for _, row in df.iterrows():
        recipient_name = row["Prospect Name"]
        recipient_email = row["Email"]
        email_body = row["Message"]

        # Create email data for Mailjet
        data = {
            'Messages': [
                {
                    "From": {
                        "Email": sender_email,
                        "Name": sender_name
                    },
                    "To": [
                        {
                            "Email": recipient_email,
                            "Name": recipient_name
                        }
                    ],
                    "Subject": f"Exclusive Opportunity for {recipient_name}!",
                    "TextPart": email_body,
                    "HTMLPart": f"<p>{email_body.replace('\n', '<br>')}</p>"
                }
            ]
        }

        # Send email through Mailjet
        result = mailjet.send.create(data=data)

        # Print status for each email
        print(f"Email to {recipient_email}: Status {result.status_code}")
        print(result.json())

# Run the function
if __name__ == "__main__":
    send_emails(sender_email="your_email@example.com", sender_name="Your Name")
