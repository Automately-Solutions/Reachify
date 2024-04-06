import yagmail

def send_email_with_yagmail():
    # Initialize yagmail with your Gmail account
    yag = yagmail.SMTP("pixelevatessolutions@gmail.com", "password")
    
    # Define the email components
    recipient = "pixelevatessolutions@gmail.com"
    subject = "Hello Pixelevate Solutions"
    content = "Congratulations Pixelevate Solutions, you just sent an email with YAGMAIL!"
    
    # Sending the email
    yag.send(to=recipient, subject=subject, contents=content)
    print("Email sent successfully!")

send_email_with_yagmail()
