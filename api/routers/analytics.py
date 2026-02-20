from fastapi import APIRouter
from database.db import get_connection,get_lead_stats

router = APIRouter()

@router.get("/analytics/{client_name}")
def analytics(client_name : str):
    return get_lead_stats(client_name)

@router.get("/conversion-rate/{client_name}")
def conversion_rate(client_name : str):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT COUNT(*) as total,
        SUM(CASE WHEN status='HOT' THEN 1 ELSE 0) as hot 
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
        "conversion_rate_percent" : round(rate,2)
    }