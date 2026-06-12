from pydantic import BaseModel

class ResponseRefreshTokenSchema(BaseModel):
    refresh_token: str
    token_type: str