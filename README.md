# SaaS Lead Automation Engine

AI-powered lead processing & automation backend.

## Features
- Lead scoring (HOT / WARM / COLD)
- Slack notification for HOT leads
- Google Sheets logging
- Auto email reply 
- Rate limiting
- Duplicate detection

## Tech Stack
FastAPI | SQLite | Slack Webhooks | Google Sheets API

## Run locally

```bash
pip install -r requirements.txt
uvicorn api.app:app --reload

## Environment Variables

Create a `.env` file in root directory:

SLACK_WEBHOOK_URL=your_slack_webhook
EMAIL_USER=your_email
EMAIL_PASS=your_app_password

## Example API Request

POST /submit-lead

{
    "name": "John Doe",
    "email": "john@email.com",
    "company": "TechCorp",
    "budget": 5000,
    "message": "We need AI Automation"
}