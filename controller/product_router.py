from fastapi import APIRouter, Depends
from dependencies.product_dependencies import get_product_service
from schemas.response.product.product_schema import ResponseProductSchema
from services.product_service import ProductService

product_router = APIRouter(prefix="/products", tags=["products"])

@product_router.get("/all", response_model=list[ResponseProductSchema])
def get_all_products(product_service: ProductService = Depends(get_product_service)):
    return product_service.get_all_products()