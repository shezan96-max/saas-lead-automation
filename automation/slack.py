import os
import requests
from config.config import SLACK_WEBHOOK


def notify_hot_lead(data):
    if not SLACK_WEBHOOK:
        return
    message = f"""
    🔥 HOT LEAD ALERT 🔥

    Name: {data["name"]},
    Email: {data["email"]},
    Company: {data["company"]},
    Budget: {data["budget"]},
    Score: {data["score"]},
    Status: {data["status"]}

    """
    requests.post(SLACK_WEBHOOK,json={"text": message})

   