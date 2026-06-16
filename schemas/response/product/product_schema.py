from pydantic import BaseModel
from models.product import PizzaSize

class ResponseProductSchema(BaseModel):
    name: str
    description: str
    price: float
    size: PizzaSize
    active: bool