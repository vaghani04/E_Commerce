from fastapi import APIRouter, Depends
from app.controllers.order_controller import OrderController
from app.models.schemas.order_schemas import OrderResponseSchema
from app.usecases.user_auth.verify_access_token import get_current_user
from typing import List

order_router = APIRouter()


@order_router.post("/orders/", response_model=OrderResponseSchema)
async def place_order(order_controller: OrderController = Depends(), current_user: dict = Depends(get_current_user)):
    return await order_controller.place_order({"current_user": current_user})

@order_router.get("/orders/", response_model=List[OrderResponseSchema])
async def get_buyer_orders(order_controller: OrderController = Depends(), current_user: dict = Depends(get_current_user)):
    return await order_controller.get_buyer_orders({"current_user": current_user})

@order_router.get("/orders/{order_id}", response_model=OrderResponseSchema)
async def get_order_details(order_id: str, order_controller: OrderController = Depends(), current_user: dict = Depends(get_current_user)):
    return await order_controller.get_order_details({"current_user": current_user, "order_id": order_id})
