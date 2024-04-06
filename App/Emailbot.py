import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Your email credentials
gmail_user = 'your_email@gmail.com'
gmail_app_password = 'your_app_password'

# Email content setup
sent_from = gmail_user
to = ['recipient_email@example.com']
subject = 'Hello from Python!'
body = 'This is a test email sent from a Python script using smtplib.'

email_text = MIMEMultipart()
email_text['From'] = sent_from
email_text['To'] = ", ".join(to)
email_text['Subject'] = subject
email_text.attach(MIMEText(body, 'plain'))

try:
    # Setup the SMTP server
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()  # Can be omitted
    server.starttls()  # Secure the connection
    server.ehlo()  # Can be omitted
    server.login
