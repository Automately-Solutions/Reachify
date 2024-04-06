import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Your email credentials
gmail_user = 'raoabdulhadi952@gmail.com'
gmail_app_password = 'app password'

# Email content setup
sent_from = gmail_user
to = ['pixelevatessolutions@gmail.com']
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
    server.login(gmail_user, gmail_app_password)
    
    # Send the email
    server.sendmail(sent_from, to, email_text.as_string())
    server.close()

    print('Email sent successfully!')
except Exception as e:
    print('Something went wrong...', e)