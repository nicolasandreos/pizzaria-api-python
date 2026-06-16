from fastapi import APIRouter, Depends
from dependencies.product_dependencies import get_product_service
from models.product import PizzaSize
from schemas.response.product.product_schema import ResponseProductSchema
from services.product_service import ProductService
from fastapi_pagination import Page, paginate

product_router = APIRouter(prefix="/products", tags=["products"])

@product_router.get("/all", response_model=list[ResponseProductSchema])
def get_all_products(product_service: ProductService = Depends(get_product_service)):
    return product_service.get_all_products()

#Pegar produtos por pagina e itens por pagina
@product_router.get("/all-paginated", response_model=Page[ResponseProductSchema])
def get_all_products_paginated(product_service: ProductService = Depends(get_product_service)):
    return paginate(product_service.get_all_products())


@product_router.get("/{size}", response_model=list[ResponseProductSchema])
def get_products_by_size(size: PizzaSize, product_service: ProductService = Depends(get_product_service)):
    return product_service.get_products_by_size(size)

