from fastapi import HTTPException
from database.db import get_connection

def verify_api_key(client_name: str, provided_key : str):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT api_key, is_active FROM clients WHERE client_name = %s", (client_name,))

    row = cursor.fetchone()
    conn.close()
    if not row:
        raise HTTPException(status_code=404, detail="Client not found")
    
    stored_key, is_active = row
    if not is_active:
        raise HTTPException(status_code=403,detail="Client inactive")

    if  stored_key != provided_key:
        raise HTTPException(status_code=403, detail="Invalid API Key")
    