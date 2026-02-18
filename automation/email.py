import requests
from config.config import BREVO_API_KEY

def send_email(to_email,subject,body):
    url = "https://api.brevo.com/v3/smtp/email"

    headers = {
        "accept": "application/json",
        "api-key": BREVO_API_KEY,
        "content-type": "application/json"
    }

    payload = {
        "sender": {"email":"agentsupremo21@gmail.com"},
        "to": [{"email":to_email}],
        "subject": subject,
        "textContent": body
    }

    response = requests.post(url,json=payload,headers=headers,timout=15)

    print(response.status_code)
    print(response.text)

    if response.status_code not in [200,201]:
        raise Exception("Email sending failed")