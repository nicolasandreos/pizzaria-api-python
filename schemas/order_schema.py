from pydantic import BaseModel

class RequestCreateOrderSchema(BaseModel):
    user_id: int
    price: float

    class Config:
        from_attributes = True