from pydantic import BaseModel


class OrderItemCreateSchema(BaseModel):
    product_id: int
    quantity: int
    
    class Config:
        from_attributes = True


class RequestCreateOrderSchema(BaseModel):
    items: list[OrderItemCreateSchema]

    class Config:
        from_attributes = True

