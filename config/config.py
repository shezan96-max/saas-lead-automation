from dotenv import load_dotenv
import os

load_dotenv()

ADMIN_API_KEY = os.getenv("ADMIN_API_KEY")
SLACK_WEBHOOK = os.getenv("SLACK_WEBHOOK")
GOOGLE_SHEET_ID=os.getenv("GOOGLE_SHEET_ID")
RESEND_API_KEY=os.getenv("RESEND_API_KEY")