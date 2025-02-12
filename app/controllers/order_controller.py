from fastapi import Depends, HTTPException, status
from app.usecases.orders.order_usecase import OrderUseCase
from app.usecases.orders.get_buyer_orders import BuyerOrderUsecase
from app.usecases.orders.get_order_details import OrderDetailUsecase
from app.usecases.orders.update_order_status import UpdateOrderStatusUsecase

class OrderController:
    def __init__(self, order_usecase: OrderUseCase = Depends(), get_buyer_order: BuyerOrderUsecase = Depends(), get_order_details: OrderDetailUsecase = Depends(), update_order_status : UpdateOrderStatusUsecase = Depends()):
        self.order_usecase = order_usecase
        self.get_buyer_order_usecase = get_buyer_order
        self.get_order_details_usecase = get_order_details
        self.update_order_status_usecase = update_order_status

    async def place_order(self, data: dict):
        if(data["current_user"]["role"] == "seller"):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only Buyers & Admins can place the order.")
        return await self.order_usecase.place_order({"user_id": data["current_user"]["sub"]})

    async def get_buyer_orders(self, data: dict):
        if(data["current_user"]["role"] == "seller"):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only Buyers & Admins can get the order details.")
        return await self.get_buyer_order_usecase.get_buyer_orders({"user_id": data["current_user"]["sub"]})

    async def get_order_details(self, data: dict):
        if(data["current_user"]["role"] == "seller"):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only Buyers & Admins can get the order details.")
        return await self.get_order_details_usecase.get_order_details({"user_id": data["current_user"]["sub"], "order_id": data["order_id"]})

    async def update_order_status(self, data: dict):
        if data["current_user"]["role"] != "admin":
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only Admins can update order status.")
        return await self.update_order_status_usecase.update_order_status({"order_id": data["order_id"], "status": data["status"]})
