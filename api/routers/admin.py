from fastapi import APIRouter
from database.db import get_connection

router = APIRouter()

@router.get("/webhook-logs")
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