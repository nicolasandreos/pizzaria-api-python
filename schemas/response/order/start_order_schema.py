from pydantic import BaseModel
from typing import List
from models.enums.order_status import OrderStatus
from schemas.response.order.get_order_schema import OrderItemResponseSchema

class ResponseStartOrderSchema(BaseModel):
    order_id: int
    user_id: int
    order_price: float
    items: List[OrderItemResponseSchema]
    order_status: OrderStatus