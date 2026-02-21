from fastapi import HTTPException
from database.db import get_connection

def verify_api_key(provided_key : str):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT client_name FROM clients WHERE api_key = %s", (provided_key,))

    row = cursor.fetchone()
    conn.close()
    if not row:
        raise HTTPException(status_code=403, detail="Invalid API Key")
    
    return row[0]
    