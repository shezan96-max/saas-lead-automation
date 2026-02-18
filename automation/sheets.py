import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime

SHEET_NAME = "SaaS_Leads"

def log_to_sheet(data):
    scope = [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/drive"
    ]

    creds = ServiceAccountCredentials.from_json_keyfile_name("config/service_account.json",scope)

    client = gspread.authorize(creds)

    sheet = client.open(SHEET_NAME).sheet1

    sheet.append_row([
        data.name,
        data.email,
        data.company,
        data.budget,
        data.message,
        str(datetime.now())
    ])