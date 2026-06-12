from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from dependencies.session_dependencies import get_session
from dependencies.security_dependencies import verify_token
from models import Order, Product, User, OrderProduct
from models.enums.order_status import OrderStatus
from schemas.order_schema import RequestCreateOrderSchema

order_router = APIRouter(prefix="/order", tags=["order"], dependencies=[Depends(verify_token)])

@order_router.post("/create")
async def create_order(order_schema: RequestCreateOrderSchema, session: Session = Depends(get_session), user: User = Depends(verify_token)):

    if user.active == False:
        raise HTTPException(status_code=403, detail="User is not active and is forbidden to create an order")
    
    total_price = 0
    for product in order_schema.items:
        product_db = session.query(Product).filter(Product.id == product.product_id).first()
        if not product_db:
            raise HTTPException(status_code=404, detail="Product not found")
        total_price += product_db.price * product.quantity

    new_order = Order(user_id=user.id, price=total_price)

    session.add(new_order)
    session.flush()

    for product in order_schema.items:
        product_db = session.query(Product).filter(Product.id == product.product_id).first()

        if not product_db:
            raise HTTPException(status_code=404, detail="Product not found")

        order_product = OrderProduct(order_id=new_order.id, product_id=product_db.id, quantity=product.quantity, unit_price=product_db.price)
        session.add(order_product)

    session.commit()

    return {
        "message": "Order created successfully",
        "order_id": new_order.id,
        "user_id": user.id,
        "order_price": new_order.price,
        "items": [
            {
                "product_id": product.product_id,
                "quantity": product.quantity,
                "unit_price": product_db.price
            }
            for product in order_schema.items
        ]
    }


@order_router.post("/cancel/{order_id}")
async def cancel_order(order_id: int, session: Session = Depends(get_session), user: User = Depends(verify_token)):
    is_user_admin = bool(user.admin)

    order = session.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    is_user_order = order.user_id == user.id

    if not is_user_admin and not is_user_order:
        raise HTTPException(status_code=403, detail="You are not authorized to cancel this order")

    if order.status not in [OrderStatus.PENDING, OrderStatus.IN_PROGRESS]:
        raise HTTPException(status_code=400, detail="Order is not pending or in progress and cannot be cancelled")

    order.status = OrderStatus.CANCELLED
    session.commit()
    return {
        "message": "Order cancelled successfully",
        "order_id": order.id,
        "order_status": order.status,
        "order_price": order.price,
    }

@order_router.get("/all")
async def get_all_orders(session: Session = Depends(get_session), user: User = Depends(verify_token)):
    if user.admin == False:
        raise HTTPException(status_code=403, detail="You are not authorized to get all orders")
    orders = session.query(Order).all()
    return {
        "orders": orders
    }

