from pydantic import BaseModel
from typing import List
from models.enums.order_status import OrderStatus

class ResponseOrderSchema(BaseModel):
    order_id: int
    user_id: int
    order_price: float
    order_status: OrderStatus

class ResponseGetAllOrdersSchema(BaseModel):
    orders: List[ResponseOrderSchema] 