from pydantic import BaseModel, field_validator
from exceptions.validation_exception import InvalidTypeException


class OrderItemCreateSchema(BaseModel):
    product_id: int
    quantity: int
    
    class Config:
        from_attributes = True


class RequestCreateOrderSchema(BaseModel):
    items: list[OrderItemCreateSchema]

    class Config:
        from_attributes = True

    @field_validator("items", mode="before")
    @classmethod
    def validate_items(cls, value) -> list[OrderItemCreateSchema]:
        if not isinstance(value, list):
            raise InvalidTypeException(expected_type=list, actual_type=type(value), field_name="items")
        return value
