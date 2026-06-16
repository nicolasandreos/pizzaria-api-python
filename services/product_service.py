import logging

from exceptions.product_exception import ProductAlreadyDisabledException, ProductAlreadyEnabledException
from exceptions.user_exceptions import ProductNotFoundException
from repositories.product_repository import ProductRepository
from schemas.request.product.product_schema import RequestProductSchema
from schemas.response.product.product_schema import ResponseProductSchema
from models.product import PizzaSize

logger = logging.getLogger(__name__)


class ProductService:
    def __init__(self, product_repository: ProductRepository):
        self._product_repository = product_repository

    def get_all_products(self) -> list[ResponseProductSchema]:
        products = self._product_repository.get_all_products()
        logger.debug("Products listed (count=%s)", len(products))
        return [ResponseProductSchema(
            name=product.name,
            description=product.description,
            price=product.price,
            size=product.size,
            active=product.active
        ) for product in products]

    def search_products(self, size: PizzaSize | None = None, name: str | None = None) -> list[ResponseProductSchema]:
        if size:
            logger.debug("Product search by size (size=%s)", size)
            products = self._product_repository.get_products_by_size(size)
        elif name:
            logger.debug("Product search by name (name=%s)", name)
            products = self._product_repository.get_products_by_name(name)
            
        return [ResponseProductSchema(
            name=product.name,
            description=product.description,
            price=product.price,
            size=product.size,
            active=product.active
        ) for product in products]

    def create_product(self, product: RequestProductSchema) -> ResponseProductSchema:
        logger.info(
            "Product creation requested (name=%s, size=%s, price=%s)",
            product.name,
            product.size,
            product.price,
        )
        product = self._product_repository.create_product(product)
        logger.info("Product created (name=%s, size=%s, active=%s)", product.name, product.size, product.active)
        return ResponseProductSchema(
            name=product.name,
            description=product.description,
            price=product.price,
            size=product.size,
            active=product.active
        )

    def update_product(self, id: int, product: RequestProductSchema) -> ResponseProductSchema:
        logger.info("Product update requested (product_id=%s, name=%s)", id, product.name)
        product_db = self._product_repository.get_product_by_id(id)
        if not product_db:
            logger.warning("Product update failed: not found (product_id=%s)", id)
            raise ProductNotFoundException()

        updated_product = self._product_repository.update_product(product_db, product)
        logger.info("Product updated (product_id=%s, name=%s)", id, updated_product.name)

        return ResponseProductSchema(
            name=updated_product.name,
            description=updated_product.description,
            price=updated_product.price,
            size=updated_product.size,
            active=updated_product.active
        )


    def disable_product(self, id: int) -> ResponseProductSchema:
        logger.info("Product disable requested (product_id=%s)", id)
        product_db = self._product_repository.get_product_by_id(id)
        if not product_db:
            logger.warning("Product disable failed: not found (product_id=%s)", id)
            raise ProductNotFoundException()

        if not product_db.active:
            logger.warning("Product disable skipped: already disabled (product_id=%s)", id)
            raise ProductAlreadyDisabledException()

        disabled_product = self._product_repository.disable_product(product_db)
        logger.info("Product disabled (product_id=%s, name=%s)", id, disabled_product.name)
        return ResponseProductSchema(
            name=disabled_product.name,
            description=disabled_product.description,
            price=disabled_product.price,
            size=disabled_product.size,
            active=disabled_product.active
        )

    def enable_product(self, id: int) -> ResponseProductSchema:
        logger.info("Product enable requested (product_id=%s)", id)
        product_db = self._product_repository.get_product_by_id(id)
        if not product_db:
            logger.warning("Product enable failed: not found (product_id=%s)", id)
            raise ProductNotFoundException()

        if product_db.active:
            logger.warning("Product enable skipped: already enabled (product_id=%s)", id)
            raise ProductAlreadyEnabledException()

        enabled_product = self._product_repository.enable_product(product_db)
        logger.info("Product enabled (product_id=%s, name=%s)", id, enabled_product.name)
        return ResponseProductSchema(
            name=enabled_product.name,
            description=enabled_product.description,
            price=enabled_product.price,
            size=enabled_product.size,
            active=enabled_product.active
        )

    def get_best_selling_product(self) -> ResponseProductSchema:
        logger.info("Fetching best-selling product")
        product = self._product_repository.get_best_selling_product()
        logger.info("Best-selling product resolved (name=%s, size=%s)", product.name, product.size)
        return ResponseProductSchema(
            name=product.name,
            description=product.description,
            price=product.price,
            size=product.size,
            active=product.active
        )