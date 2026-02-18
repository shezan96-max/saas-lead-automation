import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from config.config import EMAIL_SENDER,EMAIL_PASSWORD

SMTP_SERVER = "smtp-relay.brevo.com"
SMTP_PORT = 587

def send_email(to_email,subject,body):
    message = MIMEMultipart()
    message["From"] = EMAIL_SENDER
    message["To"] = to_email
    message["Subject"] = subject
    
    message.attach(MIMEText(body,"plain"))
    try:
        server = smtplib.SMTP(SMTP_SERVER,SMTP_PORT,timeout=30)
        server.starttls()
        server.login(EMAIL_SENDER,EMAIL_PASSWORD)
        server.sendmail(EMAIL_SENDER,to_email,message.as_string())
        server.quit()
    except Exception as e:
        print("Email error:",str(e))
        raise e