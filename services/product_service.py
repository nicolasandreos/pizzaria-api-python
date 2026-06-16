from exceptions.product_exception import ProductAlreadyDisabledException, ProductAlreadyEnabledException
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
            size=product.size,
            active=product.active
        ) for product in products]

    def get_products_by_size(self, size: PizzaSize) -> list[ResponseProductSchema]:
        products = self._product_repository.get_products_by_size(size)
        return [ResponseProductSchema(
            name=product.name,
            description=product.description,
            price=product.price,
            size=product.size,
            active=product.active
        ) for product in products]

    def create_product(self, product: RequestProductSchema) -> ResponseProductSchema:
        product = self._product_repository.create_product(product)
        return ResponseProductSchema(
            name=product.name,
            description=product.description,
            price=product.price,
            size=product.size,
            active=product.active
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
            size=updated_product.size,
            active=updated_product.active
        )


    def disable_product(self, id: int) -> ResponseProductSchema:
        product_db = self._product_repository.get_product_by_id(id)
        if not product_db:
            raise ProductNotFoundException()

        if not product_db.active:
            raise ProductAlreadyDisabledException()

        disabled_product = self._product_repository.disable_product(product_db)
        return ResponseProductSchema(
            name=disabled_product.name,
            description=disabled_product.description,
            price=disabled_product.price,
            size=disabled_product.size,
            active=disabled_product.active
        )

    def enable_product(self, id: int) -> ResponseProductSchema:
        product_db = self._product_repository.get_product_by_id(id)
        if not product_db:
            raise ProductNotFoundException()

        if product_db.active:
            raise ProductAlreadyEnabledException()

        enabled_product = self._product_repository.enable_product(product_db)
        return ResponseProductSchema(
            name=enabled_product.name,
            description=enabled_product.description,
            price=enabled_product.price,
            size=enabled_product.size,
            active=enabled_product.active
        )

    def get_best_selling_product(self) -> ResponseProductSchema:
        product = self._product_repository.get_best_selling_product()
        return ResponseProductSchema(
            name=product.name,
            description=product.description,
            price=product.price,
            size=product.size,
            active=product.active
        )