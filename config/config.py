from dotenv import load_dotenv
import os

load_dotenv()

ADMIN_API_KEY = os.getenv("ADMIN_API_KEY")
EMAIL_SENDER = os.getenv("EMAIL_SENDER")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
SLACK_WEBHOOK = os.getenv("SLACK_WEBHOOK")