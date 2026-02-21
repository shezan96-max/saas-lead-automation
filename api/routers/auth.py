from fastapi import APIRouter, HTTPException, Header
from database.db import get_connection
from api.schemas import SignupRequest
import secrets
from datetime import datetime

router = APIRouter()

@router.post("/signup")
def signup(data : SignupRequest):
    api_key = secrets.token_hex(32)
    webhook_secret = secrets.token_hex(16)

    conn = get_connection()
    cursor = conn.cursor()

    # Check duplicate client
    cursor.execute("SELECT id FROM clients WHERE client_name = %s", (data.client_name,))

    if cursor.fetchone():
        conn.close()
        raise HTTPException(status_code=400, detail="Client already exists")
    
    cursor.execute("""
        INSERT INTO clients
        (client_name, email, api_key, webhook_url, webhook_secret, created_at)
        VALUES (%s, %s, %s, %s, %s)

    """, (
        data.client_name,
        data.email,
        api_key,
        data.webhook_url,
        webhook_secret,
        datetime.utcnow(),
    ))
    conn.commit()
    conn.close()

    return {
        "message" : "Account created successfully",
        "client_name" : data.client_name,
        "api_key" : api_key,
        "webhook_secret" : webhook_secret
    }