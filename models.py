import os

from sqlalchemy import Column, ForeignKey, Integer, String, Float, DateTime, Boolean, create_engine, Enum as sqlEnum
from sqlalchemy.orm import declarative_base
from datetime import datetime
from dotenv import load_dotenv
from enum import Enum

class OrderStatus(Enum):
    PENDING = "PENDING"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"

class Size(Enum):
    SMALL = "SMALL"
    MEDIUM = "MEDIUM"
    LARGE = "LARGE"

load_dotenv()

db = create_engine(os.getenv("DATABASE_URL"), echo=True)

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    name = Column("name", String(255), nullable=False)
    email = Column("email", String(255), nullable=False, unique=True)
    password = Column("password", String(255), nullable=False)
    created_at = Column("created_at", DateTime, nullable=False, default=datetime.now())
    active = Column("active", Boolean, nullable=False, default=True)
    admin = Column("admin", Boolean, nullable=False, default=False)
    
    def __init__(self, name: str, email: str, password: str, active: bool = True, admin: bool = False) -> None:
        self.name = name
        self.email = email
        self.password = password
        self.active = active
        self.admin = admin

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

class Product(Base):
    __tablename__ = "products"

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    name = Column("name", String(255), nullable=False)
    price = Column("price", Float, nullable=False)
    description = Column("description", String(255), nullable=False)
    size = Column("size", sqlEnum(Size), nullable=False)

    def __init__(self, name: str, price: float, description: str, size: str) -> None:
        self.name = name
        self.price = price
        self.description = description
        self.size = size

class OrderProduct(Base):
    __tablename__ = "order_products"
    order_id = Column("order_id", ForeignKey("orders.id"), nullable=False, primary_key=True)
    product_id = Column("product_id", ForeignKey("products.id"), nullable=False, primary_key=True)
    quantity = Column("quantity", Integer, nullable=False)
    unit_price = Column("unit_price", Float, nullable=False)
    
    @property
    def total_price(self) -> float:
        return self.quantity * self.unit_price