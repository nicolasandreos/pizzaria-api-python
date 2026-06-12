from pydantic import BaseModel
from typing import List

class OrderItemResponseSchema(BaseModel):
    product_id: int
    quantity: int
    unit_price: float

class ResponseCreateOrderSchema(BaseModel):
    message: str
    order_id: int
    user_id: int
    order_price: float
    items: List[OrderItemResponseSchema]

    class Config:
        from_attributes = True