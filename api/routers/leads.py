from fastapi import APIRouter, Header, BackgroundTasks
from fastapi.responses import StreamingResponse

from services.lead_pipeline import process_lead
from services.auth import verify_api_key

from database.db import init_db, get_connection, update_lead_status
from api.schemas import LeadCreate

import csv, io

router = APIRouter()

@router.post("/leads")
def submit_lead(
    lead : LeadCreate,
    background_tasks : BackgroundTasks,
    x_api_key : str = Header(...)
):
    client_name = verify_api_key(x_api_key)

    result = process_lead(lead, client_name, background_tasks)

    return {
        "success" : True,
        "version" : "v1",
        "data" : result
    }

@router.get("/leads/{client_name}")
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

@router.put("/leads/{client_name}/{lead_id}/status")
def update_status(client_name : str, lead_id : int, status : str):
    update_lead_status(client_name,lead_id,status)

    return {
        "success" : True,
        "message" : "Status updated"
    }
@router.get("/leads/export")
def export_leads(x_api_key : str = Header(...)):
    client_name = verify_api_key(x_api_key)

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, name, email, company, budget, status, created_at
        FROM leads
        WHERE client_name = %s
        ORDER BY created_at DESC

    """, (client_name,))
    rows = cursor.fetchall()
    conn.close()

    output = io.StringIO()
    writer = csv.writer(output)

    writer.writerow(["ID", "Name", "Email", "Company", "Budget", "Status", "Created At"])

    for row in rows:
        writer.writerow(row)
    output.seek(0)

    return StreamingResponse(iter([output.getvalue()]), media_type="text/csv", headers={"Content-Disposition":f"attachment; filename={client_name}_leads.csv"})
