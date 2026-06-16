from sqlalchemy.orm import Session
from models.product import Product

class ProductRepository:
    def __init__(self, session: Session):
        self._session = session

    def get_all_products(self) -> list[Product]:
        return self._session.query(Product).all()