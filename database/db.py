import sqlite3
import os

BASE_DIR = "/opt/render/project/src"
CLIENTS_DIR = os.path.join(BASE_DIR,"clients")

os.makedirs(CLIENTS_DIR,exist_ok=True)

def get_db_path(client_name : str):
    client_folder = os.path.join(CLIENTS_DIR,client_name)
    os.makedirs(client_folder,exist_ok=True)
    
    return os.path.join(client_folder,"leads.db")

def init_db(client_name : str):

    db_path = get_db_path(client_name)

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS leads (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        email TEXT,
        company TEXT,
        budget INTEGER,
        message TEXT,
        score INTEGER,
        status TEXT,
        sales_rep TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP   

    )
    """)
    conn.commit()
    conn.close()
    print("Database initialized successfully")

def save_lead(client_name : str,data : dict):
    db_path = 

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO leads (name,
        email, company, budget, message, score, status, sales_rep)
        VALUES (?,?,?,?,?,?,?,?)
    """, (
        data["name"],
        data["email"],
        data["company"],
        data["budget"],
        data["message"],
        data["score"],
        data["status"],
        data["sales_rep"]
    ))

    conn.commit()
    conn.close()
    print("Leads saved to database successfully")

def update_lead_status(client_name,lead_id,status):
    db_path = f"clients/{client_name}/leads.db"
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("""
    UPDATE leads
    SET status = ?
    WHERE id = ?
    """,(status,lead_id))

    conn.commit()
    conn.close()

def fetch_all_leads(client_name):
    db_path = f"clients/{client_name}/leads.db"
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM leads")
    rows = cursor.fetchall()

    conn.close()
    return rows

def get_lead_stats(client_name):
    db_path = f"clients/{client_name}/leads.db"

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM leads")
    total = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM leads WHERE status='HOT'")
    hot = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM leads WHERE status='WARM'")
    warm = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM leads WHERE status='COLD'")
    cold = cursor.fetchone()[0]

    cursor.execute("SELECT AVG(budget) FROM leads")
    avg_budget = cursor.fetchone()[0] or 0

    cursor.execute("SELECT AVG(score) FROM leads")
    avg_score = cursor.fetchone()[0] or 0

    conn.close()

    return {
        "total" : total,
        "hot" : hot,
        "warm" : cold,
        "cold" : cold,
        "avg_budget" : round(avg_budget,2),
        "avg_score" : round(avg_score,2)
    }

def filter_leads(client_name,status=None,min_score=None):
    db_path = f"clients/{client_name}/leads.db"

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    query = "SELECT * FROM leads WHERE 1=1"

    params = []

    if status:
        query += " AND status=?"
        params.append(status)

    if min_score:
        query += " AND score>=?"
        params.append(min_score)

    cursor.execute(query,params)
    rows = cursor.fetchall()

    conn.close()
    return rows