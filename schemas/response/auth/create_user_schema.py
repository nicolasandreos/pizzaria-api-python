from pydantic import BaseModel

class ResponseCreateUserSchema(BaseModel):
    name: str
    email: str
    active: bool
    admin: bool