from exceptions.user_exceptions import ProductNotFoundException
from repositories.product_repository import ProductRepository
from schemas.request.product.product_schema import RequestProductSchema
from schemas.response.product.product_schema import ResponseProductSchema
from models.product import PizzaSize

class ProductService:
    def __init__(self, product_repository: ProductRepository):
        self._product_repository = product_repository

    def get_all_products(self) -> list[ResponseProductSchema]:
        products = self._product_repository.get_all_products()
        return [ResponseProductSchema(
            name=product.name,
            description=product.description,
            price=product.price,
            size=product.size
        ) for product in products]

    def get_products_by_size(self, size: PizzaSize) -> list[ResponseProductSchema]:
        products = self._product_repository.get_products_by_size(size)
        return [ResponseProductSchema(
            name=product.name,
            description=product.description,
            price=product.price,
            size=product.size
        ) for product in products]

    def create_product(self, product: RequestProductSchema) -> ResponseProductSchema:
        product = self._product_repository.create_product(product)
        return ResponseProductSchema(
            name=product.name,
            description=product.description,
            price=product.price,
            size=product.size
        )

    def update_product(self, id: int, product: RequestProductSchema) -> ResponseProductSchema:
        product_db = self._product_repository.get_product_by_id(id)
        if not product_db:
            raise ProductNotFoundException()

        updated_product = self._product_repository.update_product(product_db, product)

        return ResponseProductSchema(
            name=updated_product.name,
            description=updated_product.description,
            price=updated_product.price,
            size=updated_product.size
        )
        