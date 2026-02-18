import os
import resend
from config.config import RESEND_API_KEY

resend.api_key = RESEND_API_KEY

def send_email(to_email,subject,body):
    resend.Emails.send({
        "from": "Automation<onboarding@resend.dev>",
        "to": [to_email],
        "subject": subject,
        "html": f"<p>{body}</p>" 
    })