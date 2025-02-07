from fastapi import Depends, HTTPException
from app.services.cart_service import CartService
from app.models.schemas.cart_schemas import CartResponse

class CartUseCase:
    def __init__(self, cart_service: CartService = Depends()):
        self.cart_service = cart_service

    async def add_to_cart(self, data: dict):
        user_id = data["user_id"]
        cart_item = data["cart_item"]

        cart_data = {
            "user_id": user_id,
            "product_id": cart_item.product_id,
            "quantity": cart_item.quantity,
        }

        cart_result = await self.cart_service.add_to_cart(cart_data)

        if not cart_result:
            raise HTTPException(status_code=500, detail="Failed to add item to cart")

        return CartResponse(items=cart_result["items"], total_price=cart_result["total_price"])