from fastapi import APIRouter, Depends
from app.usecases.user_auth.verify_access_token import get_current_user
from app.models.schemas.cart_schemas import CartItemCreate, CartResponse, OrderResponse
from fastapi import Body
from app.controllers.cart_controller import CartController

cart_router = APIRouter(tags=["Cart"])

@cart_router.post("/cart/add", response_model=CartResponse)
async def add_to_cart(cart_item: CartItemCreate, cart_controller: CartController = Depends(), current_user: dict = Depends(get_current_user)):
    return await cart_controller.add_to_cart({"user_id": current_user["sub"], "cart_item": cart_item})

@cart_router.delete("/cart/remove/{product_id}")
async def remove_from_cart(product_id: str, cart_controller: CartController = Depends(), current_user: dict = Depends(get_current_user)):
    return await cart_controller.remove_from_cart({"user_id": current_user["sub"], "product_id": product_id})

@cart_router.get("/cart/")
async def get_cart(cart_controller: CartController = Depends(), current_user: dict = Depends(get_current_user)):
    return await cart_controller.get_cart({"user_id": current_user["sub"]})