import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
from config.config import GOOGLE_SHEET_ID

def log_to_sheet(data):
    scope = [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/drive"
    ]

    creds = ServiceAccountCredentials.from_json_keyfile_name("/etc/secrets/service_account.json",scope)

    client = gspread.authorize(creds)
    sheet_id = GOOGLE_SHEET_ID
    sheet = client.open(sheet_id).sheet1

    sheet.append_row([
        data.name,
        data.email,
        data.company,
        data.budget,
        data.message,
        str(datetime.now())
    ])