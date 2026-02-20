import requests
import hmac
import hashlib
import json
from database.db import get_connection
from datetime import datetime,timedelta

def get_client_webhook(client_name : str):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT webhook_url FROM clients WHERE client_name = %s", (client_name,))

    row = cursor.fetchone()
    conn.close()

    if row:
        return row[0]
    return None

def log_webhook(client_name, lead_email, status, code=None, error=None, next_retry=None):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO webhook_logs (
        client_name, lead_email,
        status, response_code, error, next_retry)
        VALUES (%s, %s, %s, %s, %s, %s)
    """, (client_name, lead_email, status, code, error, next_retry))

def send_webhook(client_name : str, lead_data : dict):
    webhook_url = get_client_webhook(client_name)
    secret = get_webhook_secret(client_name)

    if not webhook_url:
        return
    payload = json.dumps(lead_data)
    headers = {}

    if secret:
        signature = hmac.new(
            secret.encode(),
            payload.encode(),
            hashlib.sha256
        ).hexdigest()

        headers["X-Signature"] = signature

    try:
        response = requests.post(webhook_url, data=payload, headers=headers, timeout=5)
        if response.status_code == 200:
            log_webhook(client_name, lead_data["email"], "SUCCESS", response.status_code)

        else:
            next_retry_time = datetime.utcnow() + timedelta(minutes=5)

            log_webhook(client_name, lead_data['email'], "FAILED", response.status_code, None, next_retry_time)
    except Exception as e:
        next_retry_time = datetime.utcnow() + timedelta(minutes=5)
        log_webhook(client_name, lead_data["email"], "ERROR", None, str(e), next_retry_time)

def get_webhook_secret(client_name : str):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT webhook_secret FROM clients WHERE client_name = %s", (client_name,))

    row = cursor.fetchone()
    conn.close()

    if row:
        return row[0]
    return None
