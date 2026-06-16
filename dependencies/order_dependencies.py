from sqlalchemy.orm import Session
from dependencies.session_dependencies import get_session
from repositories.order_repository import OrderRepository
from repositories.product_repository import ProductRepository
from services.order_service import OrderService
from fastapi import Depends

def get_order_service(session: Session = Depends(get_session)):
    repository = OrderRepository(session)
    product_repository = ProductRepository(session)
    
    return OrderService(repository, product_repository)