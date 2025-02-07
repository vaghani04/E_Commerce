# # app/services/cart_service.py
# from app.repositories.cart_repo import CartRepository, get_cart_repo
# from app.models.schemas.cart_schemas import CartResponse, OrderResponse
# from fastapi import Depends, HTTPException

# class CartService:
#     def __init__(self, cart_repo: CartRepository = Depends()):
#         self.cart_repo = cart_repo

#     async def add_to_cart(self, user_id: str, product_id: str, quantity: int = 1):
#         return await self.cart_repo.add_to_cart(user_id, product_id, quantity)

#     async def remove_from_cart(self, user_id: str, product_id: str):
#         result = await self.cart_repo.remove_from_cart(user_id, product_id)
#         if not result:
#             raise HTTPException(status_code=404, detail="Product not found in cart")
#         return {"message": "Product removed from cart"}

#     async def get_cart(self, user_id: str):
#         cart = await self.cart_repo.get_cart(user_id)
#         return CartResponse(**cart)

#     async def create_order(self, user_id: str):
#         order_id = await self.cart_repo.create_order(user_id)
#         return order_id

#     async def get_orders(self, user_id: str):
#         return await self.cart_repo.get_orders(user_id)

#     async def get_order_details(self, user_id: str, order_id: str):
#         return await self.cart_repo.get_order_details(user_id, order_id)

# def get_cart_service():
#     return CartService()

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
