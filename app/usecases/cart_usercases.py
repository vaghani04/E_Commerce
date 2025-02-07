# # app/usecases/cart_usecase.py
# from fastapi import Depends
# from app.services.cart_service import CartService, get_cart_service
# from app.models.schemas.cart_schemas import CartResponse, OrderResponse

# class CartUseCase:
#     def __init__(self, cart_service: CartService = Depends()):
#         self.cart_service = cart_service

#     async def add_to_cart(self, user_id: str, product_id: str, quantity: int = 1):
#         return await self.cart_service.add_to_cart(user_id, product_id, quantity)

#     async def remove_from_cart(self, user_id: str, product_id: str):
#         return await self.cart_service.remove_from_cart(user_id, product_id)

#     async def get_cart(self, user_id: str) -> CartResponse:
#         return await self.cart_service.get_cart(user_id)

#     async def create_order(self, user_id: str) -> str:
#         return await self.cart_service.create_order(user_id)

#     async def get_orders(self, user_id: str):
#         return await self.cart_service.get_orders(user_id)

#     async def get_order_details(self, user_id: str, order_id: str):
#         return await self.cart_service.get_order_details(user_id, order_id)