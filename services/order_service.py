from repositories.order_repository import OrderRepository
from schemas.request.order.create_schema import RequestCreateOrderSchema

class OrderService:

    def __init__(self, order_repository: OrderRepository):
        self._repository = order_repository

    def create_order(self, order_schema: RequestCreateOrderSchema):
        return self._repository.create_order(order_schema)