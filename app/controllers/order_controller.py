from fastapi import Depends
from app.usecases.orders.order_usecase import OrderUseCase
from app.usecases.orders.get_buyer_orders import BuyerOrderUsecase
from app.usecases.orders.get_order_details import OrderDetailUsecase


class OrderController:
    def __init__(self, order_usecase: OrderUseCase = Depends(), get_buyer_order: BuyerOrderUsecase = Depends(), get_order_details: OrderDetailUsecase = Depends()):
        self.order_usecase = order_usecase
        self.get_buyer_order_usecase = get_buyer_order
        self.get_order_details_usecase = get_order_details

    async def place_order(self, data: dict):
        return await self.order_usecase.place_order(data)

    async def get_buyer_orders(self, data: dict):
        return await self.get_buyer_order_usecase.get_buyer_orders(data)

    async def get_order_details(self, data: dict):
        return await self.get_order_details_usecase.get_order_details(data)
