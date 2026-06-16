from sqlalchemy.orm import relationship
from database.base import Base
from sqlalchemy import Column, Integer, ForeignKey, Float

class OrderProduct(Base):
    __tablename__ = "order_products"
    order_id = Column("order_id", ForeignKey("orders.id"), nullable=False, primary_key=True)
    product_id = Column("product_id", ForeignKey("products.id"), nullable=False, primary_key=True)
    quantity = Column("quantity", Integer, nullable=False)
    unit_price = Column("unit_price", Float, nullable=False)

    order = relationship("Order", back_populates="order_products")
    product = relationship("Product", back_populates="order_products")
    
    @property
    def total_price(self) -> float:
        return self.quantity * self.unit_price