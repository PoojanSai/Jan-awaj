import smtplib
from email.mime.text import MIMEText
from config import EMAIL_SENDER, EMAIL_PASSWORD, TEST_EMAIL

def send_email(letter):
    msg = MIMEText(letter)
    msg["Subject"] = "New Citizen Grievance"
    msg["From"] = EMAIL_SENDER
    msg["To"] = TEST_EMAIL

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(EMAIL_SENDER, EMAIL_PASSWORD)
        server.send_message(msg)
