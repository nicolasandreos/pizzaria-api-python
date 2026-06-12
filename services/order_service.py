from repositories.order_repository import OrderRepository
from schemas.request.order.create_schema import RequestCreateOrderSchema
from models import User, Order, OrderProduct, Product
from exceptions.auth_exceptions import UserNotActiveException
from exceptions.product_exception import ProductNotFoundException
from exceptions.order_exception import OrderNotCreatedException
from exceptions.order_product import OrderProductNotCreatedException
from schemas.response.order.create_schema import ResponseCreateOrderSchema

class OrderService:

    def __init__(self, order_repository: OrderRepository):
        self._repository = order_repository

    def create_order(self, order_schema: RequestCreateOrderSchema, user: User):
        if user.active == False:
            raise UserNotActiveException()
    
        total_price = 0
        for product in order_schema.items:
            product_id = product.product_id

            product_db = self._repository.get_product_by_id(product_id)

            if not product_db:
                raise ProductNotFoundException()

            total_price += product_db.price * product.quantity

        new_order = Order(user_id=user.id, price=total_price)

        created_order = self._repository.create_order(new_order)

        if not created_order:
            raise OrderNotCreatedException()

        for product in order_schema.items:
            product_id = product.product_id

            product_db = self._repository.get_product_by_id(product_id)

            if not product_db:
                raise ProductNotFoundException()

            order_product = OrderProduct(order_id=created_order.id, product_id=product_db.id, quantity=product.quantity, unit_price=product_db.price)
            created_order_product = self._repository.create_order_product(order_product)

            if not created_order_product:
                raise OrderProductNotCreatedException()

        return ResponseCreateOrderSchema(
            message="Order created successfully",
            order_id=created_order.id,
            user_id=user.id,
            order_price=created_order.price,
            items=order_schema.items
        )