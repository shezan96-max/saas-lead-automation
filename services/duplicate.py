import sqlite3

def is_duplicate(client_name : str,email : str):
    db_path = f"clients/{client_name}/leads.db"

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM leads WHERE email=?",(email,))
    count = cursor.fetchone()[0]

    conn.close()

    return count > 0