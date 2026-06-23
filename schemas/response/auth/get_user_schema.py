from datetime import datetime
from pydantic import BaseModel


class ResponseGetUserSchema(BaseModel):
    name: str
    email: str
    created_at: datetime
    active: bool
    admin: bool
