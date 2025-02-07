from fastapi import Depends
from app.usecases.carts.cart_usecase import CartUseCase
from app.usecases.carts.remove_cart_usecase import RemoveCartUseCase
from app.usecases.carts.get_cart_usecase import GetCartUseCase

class CartController:
    def __init__(self, cart_usecase: CartUseCase = Depends(), remove_cart_usecase: RemoveCartUseCase = Depends(), get_cart_usecase: GetCartUseCase = Depends()):
        self.cart_usecase = cart_usecase
        self.remove_cart_usecase = remove_cart_usecase
        self.get_cart_usecase = get_cart_usecase

    async def add_to_cart(self, data: dict):
        return await self.cart_usecase.add_to_cart(data)
    
    async def remove_from_cart(self, data: dict):
        return await self.remove_cart_usecase.remove_from_cart(data)
    
    async def get_cart(self, data: dict):
        return await self.get_cart_usecase.get_cart(data)
