import logging

from repositories.order_repository import OrderRepository
from schemas.request.order.create_schema import RequestCreateOrderSchema
from models import User, Order, OrderProduct
from models.enums.order_status import OrderStatus
from exceptions.auth_exceptions import UserNotActiveException
from exceptions.product_exception import ProductNotFoundException
from exceptions.order_exception import NotAuthorizedToGetOrderException, OrderNotCreatedException, OrderNotFoundException, OrderNotAuthorizedToCancelException, OrderNotValidToCancelException, OrderNotValidToCompleteException, OrderNotValidToStartException
from exceptions.order_product import OrderProductNotCreatedException
from schemas.response.order.create_schema import ResponseCreateOrderSchema
from schemas.response.order.dashboard_schema import ResponseGetAllOrdersDashboardSchema
from schemas.response.order.get_all_schema import ResponseGetAllOrdersSchema, OrderSchema
from repositories.product_repository import ProductRepository
from schemas.response.order.get_order_schema import OrderItemResponseSchema, ResponseGetOrderSchema

logger = logging.getLogger(__name__)


class OrderService:

    def __init__(self, order_repository: OrderRepository, product_repository: ProductRepository):
        self._repository = order_repository
        self._product_repository = product_repository

    def create_order(self, order_schema: RequestCreateOrderSchema, user: User) -> ResponseCreateOrderSchema:
        logger.info(
            "Order creation requested (user_id=%s, item_count=%s)",
            user.id,
            len(order_schema.items),
        )
        if user.active == False:
            logger.warning("Order creation rejected: user inactive (user_id=%s)", user.id)
            raise UserNotActiveException()
    
        total_price = 0
        for product in order_schema.items:
            product_id = product.product_id

            product_db = self._product_repository.get_product_by_id(product_id)

            if not product_db:
                logger.warning(
                    "Order creation failed: product not found (user_id=%s, product_id=%s)",
                    user.id,
                    product_id,
                )
                raise ProductNotFoundException()

            total_price += product_db.price * product.quantity

        new_order = Order(user_id=user.id, price=total_price)

        created_order = self._repository.create_order(new_order)

        if not created_order:
            logger.error("Order creation failed: repository returned no order (user_id=%s)", user.id)
            raise OrderNotCreatedException()

        for product in order_schema.items:
            product_id = product.product_id

            product_db = self._product_repository.get_product_by_id(product_id)

            if not product_db:
                logger.warning(
                    "Order line item failed: product not found (order_id=%s, product_id=%s)",
                    created_order.id,
                    product_id,
                )
                raise ProductNotFoundException()

            order_product = OrderProduct(order_id=created_order.id, product_id=product_db.id, quantity=product.quantity, unit_price=product_db.price)
            created_order_product = self._repository.create_order_product(order_product)

            if not created_order_product:
                logger.error(
                    "Order line item not persisted (order_id=%s, product_id=%s)",
                    created_order.id,
                    product_db.id,
                )
                raise OrderProductNotCreatedException()

        self._repository.commit()
        logger.info(
            "Order created (order_id=%s, user_id=%s, total_price=%s, item_count=%s)",
            created_order.id,
            user.id,
            created_order.price,
            len(order_schema.items),
        )

        return ResponseCreateOrderSchema(
            message="Order created successfully",
            order_id=created_order.id,
            user_id=user.id,
            order_price=created_order.price,
            items=order_schema.items
        )

    def get_all_orders(self, admin_user: User) -> ResponseGetAllOrdersSchema:
        logger.info("Listing all orders (requested_by_user_id=%s)", admin_user.id)
        orders = self._repository.get_all_orders()
        logger.debug("Orders listed (count=%s, requested_by_user_id=%s)", len(orders), admin_user.id)
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
        logger.debug(
            "Fetching order (order_id=%s, requested_by_user_id=%s, is_admin=%s)",
            order_id,
            user.id,
            user.admin,
        )
        order = self._repository.get_order_by_id(order_id)
        if not order:
            logger.warning("Order lookup failed: not found (order_id=%s, user_id=%s)", order_id, user.id)
            raise OrderNotFoundException()

        if order.user_id != user.id and not user.admin:
            logger.warning(
                "Order access denied (order_id=%s, order_owner_id=%s, requested_by_user_id=%s)",
                order_id,
                order.user_id,
                user.id,
            )
            raise NotAuthorizedToGetOrderException()

        return ResponseGetOrderSchema(
            order_id=order_id,
            user_id=order.user_id,
            order_price=order.price,
            order_status=order.status,
            items=[OrderItemResponseSchema(
                product_name=order_product.product.name,
                quantity=order_product.quantity,
                unit_price=order_product.unit_price
            ) for order_product in order.order_products]
        )

    def start_order(self, order_id: int) -> ResponseGetOrderSchema:
        order = self._repository.get_order_by_id(order_id)
        if not order:
            logger.warning("Start order failed: not found (order_id=%s)", order_id)
            raise OrderNotFoundException()

        if not OrderStatus.is_enable_to_change_status(order.status, OrderStatus.IN_PROGRESS):
            logger.warning(
                "Start order rejected: invalid status transition (order_id=%s, current_status=%s)",
                order_id,
                order.status,
            )
            raise OrderNotValidToStartException()

        previous_status = order.status
        order.status = OrderStatus.IN_PROGRESS
        self._repository.update_order(order)
        logger.info(
            "Order status updated (order_id=%s, user_id=%s, %s -> %s)",
            order.id,
            order.user_id,
            previous_status,
            order.status,
        )

        return ResponseGetOrderSchema(
            order_id=order.id,
            user_id=order.user_id,
            order_price=order.price,
            items=[OrderItemResponseSchema(
                product_name=order_product.product.name,
                quantity=order_product.quantity,
                unit_price=order_product.unit_price
            ) for order_product in order.order_products],
            order_status=order.status
        )

    
    def complete_order(self, order_id: int) -> ResponseGetOrderSchema:
        order = self._repository.get_order_by_id(order_id)
        if not order:
            logger.warning("Complete order failed: not found (order_id=%s)", order_id)
            raise OrderNotFoundException()

        if not OrderStatus.is_enable_to_change_status(order.status, OrderStatus.COMPLETED):
            logger.warning(
                "Complete order rejected: invalid status transition (order_id=%s, current_status=%s)",
                order_id,
                order.status,
            )
            raise OrderNotValidToCompleteException()

        previous_status = order.status
        order.status = OrderStatus.COMPLETED
        self._repository.update_order(order)
        logger.info(
            "Order status updated (order_id=%s, user_id=%s, %s -> %s)",
            order.id,
            order.user_id,
            previous_status,
            order.status,
        )

        return ResponseGetOrderSchema(
            order_id=order.id,
            user_id=order.user_id,
            order_price=order.price,
            items=[OrderItemResponseSchema(
                product_name=order_product.product.name,
                quantity=order_product.quantity,
                unit_price=order_product.unit_price
            ) for order_product in order.order_products],
            order_status=order.status
        )

    
    def cancel_order(self, order_id: int, user: User) -> ResponseGetOrderSchema:
        logger.info(
            "Order cancellation requested (order_id=%s, requested_by_user_id=%s, is_admin=%s)",
            order_id,
            user.id,
            user.admin,
        )
        order = self._repository.get_order_by_id(order_id)
        if not order:
            logger.warning("Cancel order failed: not found (order_id=%s, user_id=%s)", order_id, user.id)
            raise OrderNotFoundException()

        if not OrderStatus.is_enable_to_change_status(order.status, OrderStatus.CANCELLED):
            logger.warning(
                "Cancel order rejected: invalid status transition (order_id=%s, current_status=%s)",
                order_id,
                order.status,
            )
            raise OrderNotValidToCancelException()

        if order.user_id != user.id and not user.admin:
            logger.warning(
                "Order cancellation denied (order_id=%s, order_owner_id=%s, requested_by_user_id=%s)",
                order_id,
                order.user_id,
                user.id,
            )
            raise OrderNotAuthorizedToCancelException()

        previous_status = order.status
        order.status = OrderStatus.CANCELLED
        self._repository.update_order(order)
        logger.info(
            "Order cancelled (order_id=%s, user_id=%s, %s -> %s, cancelled_by_user_id=%s)",
            order.id,
            order.user_id,
            previous_status,
            order.status,
            user.id,
        )

        return ResponseGetOrderSchema(
            order_id=order.id,
            user_id=order.user_id,
            order_price=order.price,
            items=[OrderItemResponseSchema(
                product_name=order_product.product.name,
                quantity=order_product.quantity,
                unit_price=order_product.unit_price
            ) for order_product in order.order_products],
            order_status=order.status
        )

    def get_all_orders_dashboard(self) -> ResponseGetAllOrdersDashboardSchema:
        logger.info("Fetching orders dashboard metrics")
        total_orders = self._repository.get_count_total_orders()
        completed_orders = self._repository.get_count_completed_orders()
        cancelled_orders = self._repository.get_count_cancelled_orders()
        revenue = self._repository.get_total_revenue()
        logger.info(
            "Orders dashboard metrics loaded (total=%s, completed=%s, cancelled=%s, revenue=%s)",
            int(total_orders),
            int(completed_orders),
            int(cancelled_orders),
            round(float(revenue), 2),
        )

        return ResponseGetAllOrdersDashboardSchema(
            total_orders=int(total_orders),
            completed_orders=int(completed_orders),
            cancelled_orders=int(cancelled_orders),
            revenue=round(float(revenue), 2)
        )
