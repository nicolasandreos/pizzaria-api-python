from fastapi import APIRouter, Depends
from dependencies.order_dependencies import get_order_service
from dependencies.admin_dependencies import get_admin_user
from dependencies.security_dependencies import verify_token
from schemas.request.order.create_schema import RequestCreateOrderSchema
from schemas.response.order.get_order_schema import ResponseGetOrderSchema
from schemas.response.order.start_order_schema import ResponseStartOrderSchema
from services.order_service import OrderService
from schemas.response.order.create_schema import ResponseCreateOrderSchema
from schemas.response.order.cancel_schema import ResponseCancelOrderSchema
from schemas.response.order.get_all_schema import ResponseGetAllOrdersSchema
from models import User

order_router = APIRouter(prefix="/order", tags=["order"], dependencies=[Depends(verify_token)])

@order_router.post("/create", response_model=ResponseCreateOrderSchema)
async def create_order(order_schema: RequestCreateOrderSchema, order_service: OrderService = Depends(get_order_service), user: User = Depends(verify_token)):
    return order_service.create_order(order_schema, user)


@order_router.post("/cancel/{order_id}", response_model=ResponseCancelOrderSchema)
async def cancel_order(order_id: int, order_service: OrderService = Depends(get_order_service), user: User = Depends(verify_token)):
    return order_service.cancel_order(order_id, user)


@order_router.get("/all", response_model=ResponseGetAllOrdersSchema)
async def get_all_orders(order_service: OrderService = Depends(get_order_service), admin_user: User = Depends(get_admin_user)):
    return order_service.get_all_orders(admin_user)


@order_router.get("/{order_id}", response_model=ResponseGetOrderSchema)
async def get_order(order_id: int, order_service: OrderService = Depends(get_order_service), user: User = Depends(verify_token)):
    return order_service.get_order(order_id, user)


@order_router.patch("/{order_id}/start", response_model=ResponseStartOrderSchema)
async def start_order(order_id: int, order_service: OrderService = Depends(get_order_service), admin_user: User = Depends(get_admin_user)):
    return order_service.start_order(order_id)
