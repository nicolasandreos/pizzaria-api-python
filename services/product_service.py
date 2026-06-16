from repositories.product_repository import ProductRepository
from schemas.response.product.product_schema import ResponseProductSchema

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

        