import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Mailjet SMTP credentials
SMTP_SERVER = "in-v3.mailjet.com"
SMTP_PORT = 587
SMTP_USER = 'API Key'
SMTP_PASSWORD = 'Secret Key'

# Email parameters
FROM_EMAIL = 'wordsmithscript@gmail.com'  # Your registered Mailjet email
TO_EMAIL = 'raoabdulhadi952@gmail.com'
SUBJECT = 'Test Email from Python'
BODY = 'This is a test email sent from Python using Mailjet SMTP.'

# Create MIME message
msg = MIMEMultipart()
msg['From'] = FROM_EMAIL
msg['To'] = TO_EMAIL
msg['Subject'] = SUBJECT
msg.attach(MIMEText(BODY, 'plain'))

# Send email
try:
    server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
    server.starttls()  # Secure the connection
    server.login(SMTP_USER, SMTP_PASSWORD)
    server.send_message(msg)
    print("Email sent successfully!")
except Exception as e:
    print(f"Failed to send email: {e}")
finally:
    server.quit()
