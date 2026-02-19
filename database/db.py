import psycopg
from config.config import DATABASE_URL


def get_connection():
    return psycopg.connect(DATABASE_URL)


def init_db():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS leads (
        id SERIAL PRIMARY KEY,
        client_name TEXT NOT NULL,
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
    print("Database initialized successfully !!")

def save_lead(client_name : str,data : dict):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO leads (client_name, name, email, company, budget, message, score, status, sales_rep) 
    VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)
    """, (
        client_name,
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
    print("Data saved to Database successfully !!!")

def update_lead_status(client_name,lead_id,status):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE leads 
        SET status=%s 
        WHERE id=%s AND client_name=%s
    """, (status, lead_id, client_name))
    
    conn.commit()
    conn.close()
    print("Lead status updated successfully !!!")

def fetch_all_leads(client_name):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM leads WHERE client_name=%s",(client_name,))
    rows = cursor.fetchall()

    conn.close()
    return rows

def get_lead_stats(client_name):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM leads WHERE client_name=%s",(client_name,))
    total = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM leads WHERE client_name=%s AND status='HOT'",(client_name,))
    hot = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM leads WHERE client_name=%s AND status='WARM'",(client_name,))
    warm = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM leads WHERE client_name=%s AND status='COLD'",(client_name,))
    cold = cursor.fetchone()[0]

    cursor.execute("SELECT AVG(budget) FROM leads WHERE client_name=%s",(client_name,))
    avg_budget = cursor.fetchone()[0] or 0

    cursor.execute("SELECT AVG(score) FROM leads WHERE client_name=%s",(client_name,))
    avg_score = cursor.fetchone()[0] or 0

    conn.close()

    return {
        "total" : total,
        "hot" : hot,
        "warm" : warm,
        "cold" : cold,
        "avg_budget" : round(avg_budget,2),
        "avg_score" : round(avg_score,2)
    }

def filter_leads(client_name,status=None,min_score=None):
    conn = get_connection()
    cursor = conn.cursor()

    query = "SELECT * FROM leads WHERE client_name=%s"
    params = [client_name]

    if status:
        query += " AND status=%s"
        params.append(status)

    if min_score:
        query += " AND score >= %s"
        params.append(min_score)

    cursor.execute(query,params)
    rows = cursor.fetchall()

    conn.close()
    return rows