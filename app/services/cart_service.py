from fastapi import Depends, HTTPException
from app.repositories.cart_repo import CartRepository

class CartService:
    def __init__(self, cart_repo: CartRepository = Depends()):
        self.cart_repo = cart_repo

    async def add_to_cart(self, data: dict) -> dict:
        return await self.cart_repo.add_to_cart(data)
    
    async def remove_from_cart(self, data: dict):
        try:
            return await self.cart_repo.remove_from_cart(data)
        except Exception:
            raise HTTPException(status_code=500, detail="Error removing item from cart")

    async def get_cart(self, data: dict):
        try:
            return await self.cart_repo.get_cart(data)
        except Exception:
            raise HTTPException(status_code=500, detail="Error fetching cart")
        
    async def get_specific_cart(self, data: dict):
        try:
            return await self.cart_repo.get_specific_cart(data)
        except Exception:
            raise HTTPException(status_code=500, detail="Error while fetching the cart")
