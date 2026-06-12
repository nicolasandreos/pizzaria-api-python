from pydantic import BaseModel, List
from models import Order

class ResponseGetAllOrdersSchema(BaseModel):
    orders: List[Order] 