from fastapi import Depends
from app.services.cart_service import CartService

class GetCartUseCase:
    def __init__(self, cart_service: CartService = Depends()):
        self.cart_service = cart_service

    async def get_cart(self, data: dict):
        return await self.cart_service.get_cart(data)
    
    async def get_specific_cart(self, data: dict):
        return await self.cart_service.get_specific_cart(data)