import smtplib 
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from config.config import EMAIL_SENDER,EMAIL_PASSWORD
import os

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

def send_email(to_email,subject,body):
    message = MIMEMultipart()
    message["From"] = EMAIL_SENDER
    message["To"] = to_email
    message["Subject"] = subject

    message.attach(MIMEText(body,"plain"))

    server = smtplib.SMTP(SMTP_SERVER,SMTP_PORT)
    server.starttls()
    server.login(EMAIL_SENDER,EMAIL_PASSWORD)
    server.sendmail(EMAIL_SENDER,to_email,message.as_string())
    server.quit()
    