from pydantic import BaseModel


class OrderItemCreateSchema(BaseModel):
    product_id: int
    quantity: int
    class Config:
        from_attributes = True
class RequestCreateOrderSchema(BaseModel):
    items: list[OrderItemCreateSchema]
    user_id: int

    class Config:
        from_attributes = True