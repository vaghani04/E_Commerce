from app.services.order_service import OrderService
from fastapi import Depends

class UpdateOrderStatusUsecase:
    def __init__(self, order_service: OrderService = Depends()):
        self.order_service = order_service

    async def update_order_status(self, data: dict):
        return await self.order_service.update_order_status(data)
