from pydantic import BaseModel

class ResponseLoginSchema(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str