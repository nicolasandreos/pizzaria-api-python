from pydantic import BaseModel

class ResponseGetAllOrdersDashboardSchema(BaseModel):
    total_orders: int
    completed_orders: int
    cancelled_orders: int
    revenue: float