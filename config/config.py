from dotenv import load_dotenv
import os

load_dotenv()

ADMIN_API_KEY = os.getenv("ADMIN_API_KEY")
SLACK_WEBHOOK = os.getenv("SLACK_WEBHOOK")
GOOGLE_SHEET_ID=os.getenv("GOOGLE_SHEET_ID")
EMAIL_SENDER=os.getenv("EMAIL_SENDER")
EMAIL_PASSWORD=os.getenv("EMAIL_PASSWORD")
BREVO_API_KEY=os.getenv("BREVO_API_KEY")