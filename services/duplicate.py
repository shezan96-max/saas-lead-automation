from database.db import get_connection

def is_duplicate(client_name : str,email : str):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT id FROM leads 
        WHERE client_name = %s 
        AND email = %s
        """, (client_name,email))
    result = cursor.fetchone()

    conn.close()

    return result is not None