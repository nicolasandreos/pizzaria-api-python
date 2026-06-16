from database.base import Base
from sqlalchemy import Column, Integer, String, Float
from .enums.pizza_size import PizzaSize
from sqlalchemy.types import Enum as sqlEnum

class Product(Base):
    __tablename__ = "products"

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    name = Column("name", String(255), nullable=False)
    price = Column("price", Float, nullable=False)
    description = Column("description", String(255), nullable=False)
    size = Column("size", sqlEnum(PizzaSize), nullable=False)

    def __init__(self, name: str, price: float, description: str, size: PizzaSize) -> None:
        self.name = name
        self.price = price
        self.description = description
        self.size = size