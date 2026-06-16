from fastapi import APIRouter, Depends, status
from dependencies.admin_dependencies import get_admin_user
from dependencies.product_dependencies import get_product_service
from dependencies.security_dependencies import verify_token
from models.product import PizzaSize
from models.user import User
from schemas.request.product.product_schema import RequestProductSchema
from schemas.response.product.product_schema import ResponseProductSchema
from services.product_service import ProductService
from fastapi_pagination import Page, paginate

product_router = APIRouter(prefix="/products", tags=["products"])

@product_router.get("/all", response_model=list[ResponseProductSchema], status_code=status.HTTP_200_OK)
def get_all_products(product_service: ProductService = Depends(get_product_service)):
    return product_service.get_all_products()


@product_router.get("/all-paginated", response_model=Page[ResponseProductSchema], status_code=status.HTTP_200_OK)
def get_all_products_paginated(product_service: ProductService = Depends(get_product_service)):
    return paginate(product_service.get_all_products())


@product_router.post("/create", response_model=ResponseProductSchema, status_code=status.HTTP_201_CREATED)
def create_product(product: RequestProductSchema, product_service: ProductService = Depends(get_product_service), admin_user: User = Depends(get_admin_user)):
    return product_service.create_product(product)


@product_router.get("/best-selling-products", response_model=ResponseProductSchema, status_code=status.HTTP_200_OK)
def get_best_selling_product(product_service: ProductService = Depends(get_product_service), user: User = Depends(verify_token)):
    return product_service.get_best_selling_product()


@product_router.get("/", response_model=list[ResponseProductSchema], status_code=status.HTTP_200_OK)
def get_products_by_size(size: PizzaSize, product_service: ProductService = Depends(get_product_service), user: User = Depends(verify_token)):
    return product_service.get_products_by_size(size)


@product_router.put("/update/{id}", response_model=ResponseProductSchema, status_code=status.HTTP_200_OK)
def update_product(id: int, product: RequestProductSchema, product_service: ProductService = Depends(get_product_service), admin_user: User = Depends(get_admin_user)):
    return product_service.update_product(id, product)


@product_router.patch("/{id}/disable", response_model=ResponseProductSchema, status_code=status.HTTP_200_OK)
def disable_product(id: int, product_service: ProductService = Depends(get_product_service), admin_user: User = Depends(get_admin_user)):
    return product_service.disable_product(id)


@product_router.patch("/{id}/enable", response_model=ResponseProductSchema, status_code=status.HTTP_200_OK)
def enable_product(id: int, product_service: ProductService = Depends(get_product_service), admin_user: User = Depends(get_admin_user)):
    return product_service.enable_product(id)