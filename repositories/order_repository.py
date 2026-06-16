from sqlalchemy import func
from sqlalchemy.orm import Session
from models import Order, OrderProduct, Product
from models.enums.order_status import OrderStatus

class OrderRepository:

    def __init__(self, session: Session) -> None:
        self._session = session

    def create_order(self, order: Order) -> Order:
        self._session.add(order)
        self._session.flush()
        return order

    def create_order_product(self, order_product: OrderProduct) -> OrderProduct:
        self._session.add(order_product)
        self._session.flush()
        return order_product

    def commit(self) -> None:
        self._session.commit()

    def get_order_by_id(self, order_id: int) -> Order | None:
        return self._session.query(Order).filter(Order.id == order_id).first()

    def update_order(self, order: Order) -> Order:
        self._session.commit()
        return order

    def get_all_orders(self) -> list[Order]:
        return self._session.query(Order).all()

    def get_count_total_orders(self) -> int:
        return self._session.query(Order).count()

    def get_count_completed_orders(self) -> int:
        return self._session.query(Order).filter(Order.status == OrderStatus.COMPLETED).count() or 0

    def get_count_cancelled_orders(self) -> int:
        return self._session.query(Order).filter(Order.status == OrderStatus.CANCELLED).count() or 0

    # Adicionar filtro onde status = completo
    def get_total_revenue(self) -> float:
        return self._session.query(func.sum(Order.price)).filter(Order.status == OrderStatus.COMPLETED).scalar() or 0
