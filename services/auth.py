from fastapi import HTTPException
from database.db import get_connection

def verify_api_key(client_name: str, x_api_key : str):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT api_key FROM clients WHERE client_name = %s", (client_name,))

    row = cursor.fetchone()
    conn.close()
    if not row:
        raise HTTPException(status_code=404, detail="Client not found")
    
    expected_key = row[0]

    if  x_api_key != expected_key:
        raise HTTPException(status_code=403, detail="Invalid API Key")
    