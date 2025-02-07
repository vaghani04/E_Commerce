from fastapi import Depends, HTTPException
from app.services.order_service import OrderService
from app.models.schemas.order_schemas import OrderResponseSchema

class OrderUseCase:
    def __init__(self, order_service: OrderService = Depends()):
        self.order_service = order_service

    async def place_order(self, data: dict):
        order = await self.order_service.place_order(data)
        if not order:
            raise HTTPException(status_code=400, detail="Failed to place order")
        return OrderResponseSchema(**order)
