from fastapi import Depends, HTTPException
from app.repositories.order_repo import OrderRepository
from app.models.schemas.order_schemas import OrderResponseSchema, OrderItemSchema
from datetime import datetime, timezone

class OrderService:
    def __init__(self, order_repo: OrderRepository = Depends()):
        self.order_repo = order_repo

    async def place_order(self, data: dict):
        return await self.order_repo.place_order(data)
    
    async def get_buyer_orders(self, data: dict):
        try:
            orders = await self.order_repo.get_buyer_orders(data)
            if not orders:
                raise HTTPException(status_code=404, detail="No orders found")
            formatted_orders = [
                OrderResponseSchema(
                    order_id=str(order["_id"]),
                    user_id=order["user_id"],
                    items=[OrderItemSchema(**item) for item in order["items"]],
                    total_price=order["total_price"],
                    status=order["status"],
                    created_at=order["created_at"]
                ) for order in orders
            ]
            return formatted_orders
        except Exception:
            raise HTTPException(status_code=500, detail="Error fetching orders")

    async def get_order_details(self, data: dict):
        try:
            # order = await self.order_repo.get_order_details(data)
            order = await self.order_repo.get_order_by_id(data)
            if not order:
                raise HTTPException(status_code=404, detail="Order not found")
            return OrderResponseSchema(
                order_id=str(order["_id"]),
                user_id=order["user_id"],
                items=[OrderItemSchema(**item) for item in order["items"]],
                total_price=order["total_price"],
                status=order["status"],
                created_at=order["created_at"],
                updated_at=order["updated_at"]
            )
        except Exception:
            raise HTTPException(status_code=500, detail="Error fetching order details")

    async def update_order_status(self, data: dict):
        if data["status"] not in ["pending", "shipped", "delivered", "cancelled"]:
            raise HTTPException(status_code=400, detail="Invalid status. Allowed values: pending, shipped, delivered, cancelled.")
        
        order = await self.order_repo.get_order_by_id(data)
        if not order:
            raise HTTPException(status_code=404, detail="Order not found")
        
        if order["status"] == data["status"]:
            raise HTTPException(status_code=400, detail="Please change the status, it's already set to the given value.")

        await self.order_repo.update_order_status({"order_id": data["order_id"], "status": data["status"], "updated_at": datetime.now(timezone.utc)})

        return await self.get_order_details(data)
