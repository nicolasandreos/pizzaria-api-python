from database.base import Base
from sqlalchemy import Column, Integer, ForeignKey, Float
from enums.order_status import OrderStatus
from sqlalchemy.types import Enum as sqlEnum

class Order(Base):
    __tablename__ = "orders"

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    user_id = Column("user_id", ForeignKey("users.id"), nullable=False)
    price = Column("price", Float, nullable=False)
    status = Column("status", sqlEnum(OrderStatus), nullable=False, default=OrderStatus.PENDING)

    def __init__(self, user_id: int, price: float, status: str = "PENDING") -> None:
        self.user_id = user_id
        self.price = price
        self.status = status