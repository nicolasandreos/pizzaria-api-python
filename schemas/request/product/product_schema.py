from pydantic import BaseModel, Field
from models.product import PizzaSize

class RequestProductSchema(BaseModel):
    name: str = Field(min_length=3, max_length=100)
    description: str = Field(min_length=3, max_length=100)
    price: float = Field(gt=0)
    size: PizzaSize