from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from dependencies.order_dependencies import get_order_service
from dependencies.session_dependencies import get_session
from dependencies.security_dependencies import verify_token
from models import Order, Product, User, OrderProduct
from models.enums.order_status import OrderStatus
from schemas.request.order.create_schema import RequestCreateOrderSchema
from services.order_service import OrderService

order_router = APIRouter(prefix="/order", tags=["order"], dependencies=[Depends(verify_token)])

@order_router.post("/create")
async def create_order(order_schema: RequestCreateOrderSchema, order_service: OrderService = Depends(get_order_service), user: User = Depends(verify_token)):
    return order_service.create_order(order_schema, user)


@order_router.post("/cancel/{order_id}")
async def cancel_order(order_id: int, order_service: OrderService = Depends(get_order_service), user: User = Depends(verify_token)):
    return order_service.cancel_order(order_id, user)


@order_router.get("/all")
async def get_all_orders(session: Session = Depends(get_session), user: User = Depends(verify_token)):
    if user.admin == False:
        raise HTTPException(status_code=403, detail="You are not authorized to get all orders")
    orders = session.query(Order).all()
    return {
        "orders": orders
    }

