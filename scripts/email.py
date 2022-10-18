from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib, ssl
import pkg.read_write as read_write


def send_email():
    email_creds = read_write.read_email_creds()
    release_notes = read_write.read_release_notes_html()

    port = 465  # For SSL

    message = MIMEMultipart("alternative")
    message["Subject"] = "Dynatrace Release Update"
    message["From"] = email_creds["sender_email"]
    message["To"] = email_creds["receiver_email"]
    body = MIMEText(release_notes,"html")
    message.attach(body)

    # Create a secure SSL context
    context = ssl.create_default_context()

    with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
        try:
            server.login(email_creds["sender_email"], email_creds["app_password"])
        except:
            print('Incorrect Username or Password:\n')
        
        server.sendmail(
            email_creds["sender_email"], email_creds["receiver_email"], message.as_string()
        )