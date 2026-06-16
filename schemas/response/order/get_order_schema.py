from pydantic import BaseModel
from typing import List
from models.enums.order_status import OrderStatus

class OrderItemResponseSchema(BaseModel):
    product_name: str
    quantity: int
    unit_price: float

class ResponseGetOrderSchema(BaseModel):
    order_id: int
    user_id: int
    order_price: float
    items: List[OrderItemResponseSchema]
    order_status: OrderStatus