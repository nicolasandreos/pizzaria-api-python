from sqlalchemy.orm import Session
from dependencies.session_dependencies import get_session
from repositories.order_repository import OrderRepository
from services.order_service import OrderService
from fastapi import Depends

def get_order_service(session: Session = Depends(get_session)):
    repository = OrderRepository(session)
    return OrderService(repository)