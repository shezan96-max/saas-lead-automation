from fastapi import FastAPI
from fastapi import Header,BackgroundTasks
from fastapi.staticfiles import StaticFiles
from fastapi.responses import StreamingResponse
from api.schemas import LeadCreate
from database.db import get_connection,init_db,update_lead_status,get_lead_stats
from services.lead_pipeline import process_lead
from services.auth import verify_api_key
import csv
import io

app = FastAPI()

@app.on_event("startup")
def startup():
    return "API Running"

@app.get("/health")
def health():
    return {"status" : "OK","message" : "API Running"}

@app.post("/submit-lead")
def submit_lead(lead : LeadCreate):
    client_name = lead.company
    init_db()

    result = process_lead(lead, client_name)
    
    return {
        "success" : True,
        "status" : "Lead saved, automation triggered",
        "data" : result
    }

@app.put("/update-status/{lead_id}")
def update_status(client_name : str,lead_id : int,status : str):
    update_lead_status(client_name,lead_id,status)

    return {
        "success" : True,
        "message" : "Status updated"
    }
@app.get("/leads/{client_name}")
def get_leads(client_name : str):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, name, email, company, budget, score, status, created_at 
        FROM leads 
        WHERE client_name = %s
        ORDER BY created_at DESC  
    """, (client_name,))
    rows = cursor.fetchall()
    conn.close()

    leads = []
    for row in rows:
        leads.append({
            "id" : row[0],
            "name" : row[1],
            "email" : row[2],
            "company" : row[3],
            "budget" : row[4],
            "score" : row[5],
            "status" : row[6],
            "created_at" : str(row[7])
        })
    return leads


@app.get("/export-hot-leads/{client_name}")
def export_csv(client_name : str):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, name, email, company, budget, score, status, created_at
        FROM leads
        WHERE client_name = %s
        ORDER BY created_at DESC""", (client_name,))

    rows = cursor.fetchall()
    conn.close()

    output = io.StringIO()
    writer = csv.writer(output)
    filename = f"{client_name}_leads.csv"

    

    writer.writerow(["ID","Name","Email","Company","Budget","Score","Status","Date"])

    writer.writerows(rows)
    output.seek(0)

    return StreamingResponse(output,media_type="text/csv",headers={"Content-Disposition" : f"attachment; filename={filename}"})

@app.get("/analytics/{client_name}")
def analytics(client_name : str):
    return get_lead_stats(client_name)

app.mount("/",StaticFiles(directory="frontend",html=True), name="frontend")


# Versioned api
@app.post("/api/v1/leads")
def submit_lead_v1(lead : LeadCreate, background_tasks : BackgroundTasks, x_api_key : str = Header(...)): # temporary placeholder
    client_name = lead.company
    verify_api_key(client_name, x_api_key)
    init_db()

    result = process_lead(lead, client_name, background_tasks)

    return {
        "success" : True,
        "version" : "v1",
        "data" : result
    }

@app.get("/api/v1/analytics/{client_name}")
def analytics_v1(client_name : str):
    return get_lead_stats(client_name)

@app.get("/api/v1/conversation-rate/{client_name}")
def conversation_rate(client_name : str):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            COUNT(*) as total,
            SUM(CASE WHEN status='HOT' THEN 1 ELSE 0 END) as hot
        FROM leads
        WHERE client_name = %s      
    """, (client_name,))

    row = cursor.fetchone()
    conn.close()

    total = row[0] or 0
    hot = row[1] or 0

    rate = (hot / total * 100) if total > 0 else 0

    return {
        "client" : client_name,
        "total_leads" : total,
        "hot_leads" : hot,
        "conversation_rate_percent" : round(rate,2)
    }

@app.get("/api/v1/admin/webhook-logs")
def get_failed_webhooks():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, client_name, lead_email, status, 
            response_code, error, retry_count, next_retry, created_at
        FROM webhook_logs
        WHERE status IN ('FAILED','ERROR')
        ORDER BY created_at DESC
                   
    """)

    rows = cursor.fetchall()
    conn.clos()

    logs = []

    for row in rows:
        logs.append({
            "id" : row[0],
            "client_name" : row[1],
            "lead_email" : row[2],
            "status" : row[3],
            "response_code" : row[4],
            "error" : row[5],
            "retry_count" : row[6],
            "next_retry" : str(row[7]) if row[7] else None,
            "created_at" : str(row[8])
        })

    return {
        "total_failed" : len(logs),
        "logs" : logs
    }