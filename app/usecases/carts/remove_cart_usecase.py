from fastapi import Depends
from app.services.cart_service import CartService

class RemoveCartUseCase:
    def __init__(self, cart_service: CartService = Depends()):
        self.cart_service = cart_service

    async def remove_from_cart(self, data: dict):
        return await self.cart_service.remove_from_cart(data)