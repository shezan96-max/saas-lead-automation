from fastapi import FastAPI
from fastapi import Header,HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import StreamingResponse
from api.schemas import LeadCreate
from database.db import get_connection,init_db,save_lead,update_lead_status,get_lead_stats,filter_leads
from automation.email import send_email
from automation.sheets import log_to_sheet
from automation.slack import notify_hot_lead
from fastapi.responses import FileResponse
from services.scoring import calculate_score
from services.status import determine_status
from services.duplicate import is_duplicate
from services.rate_limit import check_rate_limit
from services.config_loader import load_client_config
import csv
import io
import os
from config.config import ADMIN_API_KEY

app = FastAPI()

app.mount("/ui",StaticFiles(directory="frontend",html=True),name="ui")

@app.on_event("startup")
def startup():
    return "API Running"

@app.get("/health")
def health():
    return {"status" : "OK","message" : "API Running"}

@app.post("/submit-lead")
def submit_lead(lead : LeadCreate):
    client_name = lead.company
    config = load_client_config(client_name)
    init_db()

    lead_dict = lead.dict()

    # 1. Rate limit check
    if not check_rate_limit(client_name):
        raise HTTPException(status_code=429,detail="Too many requests")
    
    # 2. Duplicate check
    if is_duplicate(client_name,lead_dict["email"]):
        raise HTTPException(status_code=400,detail="Duplicate Lead")
    
    # 3. Calculate score
    score = calculate_score(lead_dict["budget"],lead_dict["message"])
    lead_dict["score"] = score

    # 4. Determine status
    status = determine_status(score)
    lead_dict["status"] = status

    # 5. Assign sales rep
    if status == "HOT":
        lead_dict["sales_rep"] = "Senior Sales"
    elif status == "WARM":
        lead_dict["sales_rep"] = "Junoir Sales"
    else:
        lead_dict["sales_rep"] = "Nurture Campaign"

    # 6. Save to DB
    save_lead(client_name, lead_dict)
    
    # 7. Slack notify only if HOT
    if status == "HOT":
        notify_hot_lead(lead_dict)

    # 8. Auto email reply to lead
    send_email(to_email=lead.email,subject="We received your inquiry!",body=f"""
        Hi {lead.name},

        Thank you for contacting us.
        We will review your message and get back to you soon.

        Regards,
        CortexLabs96
    """)
    # 9. Log to sheet
    log_to_sheet(lead)
    return {
        "success" : True,
        "status" : "Lead saved, Slack notification sent, Email sent, Sheet updated.",
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

