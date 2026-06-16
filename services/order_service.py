from repositories.order_repository import OrderRepository
from schemas.request.order.create_schema import RequestCreateOrderSchema
from models import User, Order, OrderProduct
from models.enums.order_status import OrderStatus
from exceptions.auth_exceptions import UserNotActiveException
from exceptions.product_exception import ProductNotFoundException
from exceptions.order_exception import NotAuthorizedToGetOrderException, OrderNotCreatedException, OrderNotFoundException, OrderNotAuthorizedToCancelException, OrderNotValidToCancelException
from exceptions.order_product import OrderProductNotCreatedException
from schemas.response.order.create_schema import ResponseCreateOrderSchema
from schemas.response.order.cancel_schema import ResponseCancelOrderSchema
from schemas.response.order.get_all_schema import ResponseGetAllOrdersSchema, OrderSchema
from repositories.product_repository import ProductRepository
from schemas.response.order.get_order_schema import OrderItemResponseSchema, ResponseGetOrderSchema

class OrderService:

    def __init__(self, order_repository: OrderRepository, product_repository: ProductRepository):
        self._repository = order_repository
        self._product_repository = product_repository

    def create_order(self, order_schema: RequestCreateOrderSchema, user: User) -> ResponseCreateOrderSchema:
        if user.active == False:
            raise UserNotActiveException()
    
        total_price = 0
        for product in order_schema.items:
            product_id = product.product_id

            product_db = self._product_repository.get_product_by_id(product_id)

            if not product_db:
                raise ProductNotFoundException()

            total_price += product_db.price * product.quantity

        new_order = Order(user_id=user.id, price=total_price)

        created_order = self._repository.create_order(new_order)

        if not created_order:
            raise OrderNotCreatedException()

        for product in order_schema.items:
            product_id = product.product_id

            product_db = self._product_repository.get_product_by_id(product_id)

            if not product_db:
                raise ProductNotFoundException()

            order_product = OrderProduct(order_id=created_order.id, product_id=product_db.id, quantity=product.quantity, unit_price=product_db.price)
            created_order_product = self._repository.create_order_product(order_product)

            if not created_order_product:
                raise OrderProductNotCreatedException()

        self._repository.commit()

        return ResponseCreateOrderSchema(
            message="Order created successfully",
            order_id=created_order.id,
            user_id=user.id,
            order_price=created_order.price,
            items=order_schema.items
        )

    def cancel_order(self, order_id: int, user: User) -> ResponseCancelOrderSchema:
        is_user_admin = bool(user.admin)

        order = self._repository.get_order_by_id(order_id)
        if not order:
            raise OrderNotFoundException()

        is_user_order = order.user_id == user.id

        if not is_user_admin or not is_user_order:
            raise OrderNotAuthorizedToCancelException()

        if order.status not in [OrderStatus.PENDING, OrderStatus.IN_PROGRESS]:
            raise OrderNotValidToCancelException()

        order.status = OrderStatus.CANCELLED
        self._repository.update_order(order)

        return ResponseCancelOrderSchema(
            message="Order cancelled successfully",
            order_id=order.id,
            order_status=order.status,
            order_price=order.price
        )

    def get_all_orders(self, admin_user: User) -> ResponseGetAllOrdersSchema:
        orders = self._repository.get_all_orders()
        orders_schema = [OrderSchema(
            order_id=order.id,
            user_id=order.user_id,
            order_price=order.price,
            order_status=order.status
        ) for order in orders]
        return ResponseGetAllOrdersSchema(
            orders=orders_schema
        )

    def get_order(self, order_id: int, user: User) -> ResponseGetOrderSchema:
        order = self._repository.get_order_by_id(order_id)
        if not order:
            raise OrderNotFoundException()

        if order.user_id != user.id and not user.admin:
            raise NotAuthorizedToGetOrderException()

        return ResponseGetOrderSchema(
            order_id=order_id,
            user_id=user.id,
            order_price=order.price,
            items=[OrderItemResponseSchema(
                product_name=order_product.product.name,
                quantity=order_product.quantity,
                unit_price=order_product.unit_price
            ) for order_product in order.order_products]
        )