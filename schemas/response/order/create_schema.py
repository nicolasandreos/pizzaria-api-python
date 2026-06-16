from pydantic import BaseModel
class OrderItemCreateSchema(BaseModel):
    product_id: int
    quantity: int
    
    class Config:
        from_attributes = True
class ResponseCreateOrderSchema(BaseModel):
    message: str
    order_id: int
    user_id: int
    order_price: float
    items: list[OrderItemCreateSchema]

    class Config:
        from_attributes = True