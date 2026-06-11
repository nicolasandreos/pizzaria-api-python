from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from dependencies import get_session
from models import Order, Product, User, OrderProduct
from schemas.order_schema import RequestCreateOrderSchema

order_router = APIRouter(prefix="/order", tags=["order"])

@order_router.post("/create")
async def create_order(order_schema: RequestCreateOrderSchema, session: Session = Depends(get_session)):

    user_by_id = session.query(User).filter(User.id == order_schema.user_id).first()

    if not user_by_id:
        raise HTTPException(status_code=404, detail="User not found")

    if user_by_id.active == False:
        raise HTTPException(status_code=403, detail="User is not active and is forbidden to create an order")
    
    total_price = 0
    for product in order_schema.items:
        product_db = session.query(Product).filter(Product.id == product.product_id).first()
        if not product_db:
            raise HTTPException(status_code=404, detail="Product not found")
        total_price += product_db.price * product.quantity

    new_order = Order(user_id=order_schema.user_id, price=total_price)

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
        "user_id": new_order.user_id,
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