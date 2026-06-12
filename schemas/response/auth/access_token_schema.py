from pydantic import BaseModel

class ResponseAccessTokenSchema(BaseModel):
    access_token: str
    token_type: str