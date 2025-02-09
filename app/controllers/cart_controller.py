from fastapi import Depends, HTTPException, status
from app.usecases.carts.cart_usecase import CartUseCase
from app.usecases.carts.remove_cart_usecase import RemoveCartUseCase
from app.usecases.carts.get_cart_usecase import GetCartUseCase

class CartController:
    def __init__(self, cart_usecase: CartUseCase = Depends(), remove_cart_usecase: RemoveCartUseCase = Depends(), get_cart_usecase: GetCartUseCase = Depends()):
        self.cart_usecase = cart_usecase
        self.remove_cart_usecase = remove_cart_usecase
        self.get_cart_usecase = get_cart_usecase

    async def add_to_cart(self, data: dict):
        if(data["current_user"]["role"] == "seller"):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only Buyers & Admins can add the items to the carts.")
        return await self.cart_usecase.add_to_cart({"user_id": data["current_user"]["sub"], "cart_item": data["cart_item"]})
    
    async def remove_from_cart(self, data: dict):
        if(data["current_user"]["role"] == "seller"):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only Buyers & Admins can remove the items from the carts.")
        cart_item = await self.get_cart_usecase.get_specific_cart({"user_id": data["current_user"]["sub"], "product_id": data["product_id"]})
        if cart_item is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cart Item not found for the current user.")
        
        if (data["current_user"]["role"] != "admin" and cart_item["user_id"] != data["current_user"]["sub"]) or (data["current_user"]["role"] =="buyer" and cart_item["user_id"] != data["current_user"]["sub"]):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only the buyer who made the cart can update it")
    
        return await self.remove_cart_usecase.remove_from_cart({"user_id": data["current_user"]["sub"], "cart_item": data["cart_item"]})
    
    async def get_cart(self, data: dict):
        if(data["current_user"]["role"] == "seller"):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only Buyers & Admins can add the items to the carts.")
        return await self.get_cart_usecase.get_cart({"user_id": data["current_user"]})
    
    async def get_specific_cart(self, data: dict):
        return await self.get_cart_usecase.get_specific_cart(data)
