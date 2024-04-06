from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from email.mime.text import MIMEText
import base64

# The CLIENT_CONFIG information should be obtained from your OAuth2 credentials
CLIENT_CONFIG = {
    "installed": {
        "client_id": "149835260043-ouii4aoeemlokh3167bucoms45g3pu54.apps.googleusercontent.com",
        "project_id": "reachify-419519",
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
        "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
        "client_secret": "-",
        "redirect_uris": ["urn:ietf:wg:oauth:2.0:oob", "http://localhost"]
    }
}

SCOPES = ['https://www.googleapis.com/auth/gmail.send']

def create_message(sender, to, subject, message_text):
    message = MIMEText(message_text)
    message['to'] = to
    message['from'] = sender
    message['subject'] = subject
    return {'raw': base64.urlsafe_b64encode(message.as_bytes()).decode()}

def send_message(service, user_id, message):
    try:
        message = (service.users().messages().send(userId=user_id, body=message).execute())
        print('Message Id: %s' % message['id'])
        return message
    except HttpError as error:
        print(f'An error occurred: {error}')

def main():
    flow = InstalledAppFlow.from_client_config(CLIENT_CONFIG, SCOPES)
    credentials = flow.run_local_server(port=0)

    try:
        service = build('gmail', 'v1', credentials=credentials)
        sender = "wordsmithscript@gmail.com"
        to = "raoabdulhadi952@example.com"
        subject = "Test Email"
        message_text = "Hello, this is a test email."
        message = create_message(sender, to, subject, message_text)
        send_message(service, "me", message)
    except HttpError as error:
        print(f'An error occurred: {error}')

if __name__ == '__main__':
    main()
