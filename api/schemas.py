from pydantic import BaseModel,EmailStr
from typing import Optional

class LeadCreate(BaseModel):
    name : str
    email : EmailStr
    company : Optional[str] = None
    budget : Optional[float] = None
    message : str
    source : str
    campaign_id : str | None = None

class SignupRequest(BaseModel):
    client_name : str
    email : EmailStr
    webhook_url : str | None = None
    webhook_secret : str | None = None