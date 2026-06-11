from pydantic import BaseModel

class RequestLoginSchema(BaseModel):
    email: str
    password: str