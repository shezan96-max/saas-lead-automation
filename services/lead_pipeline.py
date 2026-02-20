from fastapi import HTTPException

from services.rate_limit import check_rate_limit
from services.duplicate import is_duplicate
from services.scoring import calculate_score
from services.status import determine_status
from services.webhook import send_webhook

from database.db import save_lead

from automation.slack import notify_hot_lead
from automation.email import send_email
from automation.sheets import log_to_sheet

def process_lead(lead, client_name, background_tasks=None):

    lead_dict = lead.dict()

    # 1. Rate limit
    if not check_rate_limit(client_name):
        raise HTTPException(status_code=429, detail="Too many requests")
    
    # 2. Duplicate
    if is_duplicate(client_name, lead_dict["email"]):
        raise HTTPException(status_code=400, detail="Duplicate Lead")
    
    # 3. Score
    score = calculate_score(lead_dict["budget"], lead_dict["message"])
    lead_dict["score"] = score

    # 4. Status
    status = determine_status(score)
    lead_dict["status"] = status

    # 5. Assign sales rep
    if status == "HOT":
        lead_dict["sales_rep"] = "Senior Sales"
    elif status == "WARM":
        lead_dict["sales_rep"] = "Junior Sales"
    else:
        lead_dict["sales_rep"] = "Nurture Campaign"

    # 6. Save to DB
    save_lead(client_name, lead_dict)

    # 7. Slack notify if HOT
    if status == "HOT":
        notify_hot_lead(lead_dict)

        if background_tasks:
            background_tasks.add_task(send_webhook, client_name, lead_dict)
        else:
            send_webhook(client_name, lead_dict)
    
    # 8. Email auto reply:
    send_email(
        to_email=lead.email,
        subject="We received your inquiry!",
        body=f"""
            Hi {lead.name},

            Thank you for contacting us.
            We will review your message and get back to you soon.

            Regards,
            CortexLabs96
        """
        )
    # Log to sheet
    log_to_sheet(lead)
    
    return lead_dict
