from pydantic import BaseModel
from models.enums.order_status import OrderStatus

class ResponseCancelOrderSchema(BaseModel):
    message: str
    order_id: int
    order_status: OrderStatus
    order_price: float