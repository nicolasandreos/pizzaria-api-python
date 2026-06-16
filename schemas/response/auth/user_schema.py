from pydantic import BaseModel
from datetime import datetime

class ResponseUserSchema(BaseModel):
    name: str
    email: str
    active: bool
    admin: bool
    created_at: datetime