from app.services.order_service import OrderService
from fastapi import Depends

class BuyerOrderUsecase:
    def __init__(self, order_service: OrderService = Depends()):
        self.order_service = order_service

    async def get_buyer_orders(self, data: dict):
        return await self.order_service.get_buyer_orders(data)
