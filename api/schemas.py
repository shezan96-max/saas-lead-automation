from pydantic import BaseModel,EmailStr
from typing import Optional

class LeadCreate(BaseModel):
    name : str
    email : EmailStr
    company : Optional[str] = None
    budget : Optional[float] = None
    message : str

