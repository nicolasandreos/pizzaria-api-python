from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from dependencies import get_session
from models import Order, User
from schemas.order_schema import OrderSchema

order_router = APIRouter(prefix="/order", tags=["order"])

@order_router.post("/create")
async def create_order(order_schema: OrderSchema, session: Session = Depends(get_session)):

    user_by_id = session.query(User).filter(User.id == order_schema.user_id).first()

    if not user_by_id:
        raise HTTPException(status_code=404, detail="User not found")

    new_order = Order(user_id=order_schema.user_id, price=order_schema.price)

    session.add(new_order)
    session.commit()

    return HTTPException(status_code=201, detail=f"Order created successfully from User ID: {new_order.user_id} Order ID: {new_order.id} Price: {new_order.price}")