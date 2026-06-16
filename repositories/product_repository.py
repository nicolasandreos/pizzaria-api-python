from sqlalchemy.orm import Session
from models.product import Product
from models.product import PizzaSize
from schemas.request.product.product_schema import RequestProductSchema

class ProductRepository:
    def __init__(self, session: Session):
        self._session = session

    def get_product_by_id(self, id: int) -> Product:
        return self._session.query(Product).filter(Product.id == id).first()

    def get_all_products(self) -> list[Product]:
        return self._session.query(Product).all()

    def get_products_by_size(self, size: PizzaSize) -> list[Product]:
        return self._session.query(Product).filter(Product.size == size).all()

    def create_product(self, product: RequestProductSchema) -> Product:
        new_product = Product(
            name=product.name,
            description=product.description,
            price=product.price,
            size=product.size
        )
        self._session.add(new_product)
        self._session.commit()
        return new_product

    def update_product(self, product_db: Product, product: RequestProductSchema) -> Product:
        product_db.name = product.name
        product_db.description = product.description
        product_db.price = product.price
        product_db.size = product.size
        self._session.commit()
        return product_db

    
    def disable_product(self, product_db: Product) -> Product:
        product_db.active = False
        self._session.commit()
        return product_db

    
    def enable_product(self, product_db: Product) -> Product:
        product_db.active = True
        self._session.commit()
        return product_db