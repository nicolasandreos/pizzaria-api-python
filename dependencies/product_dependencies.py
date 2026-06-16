from repositories.product_repository import ProductRepository
from services.product_service import ProductService
from sqlalchemy.orm import Session
from dependencies.session_dependencies import get_session
from fastapi import Depends


def get_product_service(session: Session = Depends(get_session)) -> ProductService:
    product_repository = ProductRepository(session)
    product_service = ProductService(product_repository)
    return product_service