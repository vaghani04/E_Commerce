from fastapi import HTTPException
from app.config.database import db_helper
from bson import ObjectId
from datetime import datetime, timezone

class OrderRepository:
    def __init__(self):
        self.cart_collection = db_helper.carts
        self.order_collection = db_helper.orders
        self.product_collection = db_helper.products

    async def place_order(self, data: dict):
        try:
            cart_items = await self.cart_collection.find({"user_id": data["user_id"]}).to_list(length=None)
            if not cart_items:
                raise HTTPException(status_code=400, detail="Cart is empty")

            order_items = []
            total_price = 0

            for item in cart_items:
                product = await self.product_collection.find_one({"_id": item["product_id"]})
                if not product:
                    raise HTTPException(status_code=404, detail="Product not found")

                subtotal = item["quantity"] * product["price"]
                total_price += subtotal

                order_items.append({
                    "product_id": str(item["product_id"]),
                    "product_name": product["title"],
                    "product_price": product["price"],
                    "quantity": item["quantity"],
                    "subtotal": subtotal
                })

            order_data = {
                "user_id": data["user_id"],
                "items": order_items,
                "total_price": total_price,
                "status": "Pending",
                "created_at": datetime.now(timezone.utc)
            }

            result = await self.order_collection.insert_one(order_data)
            if not result.inserted_id:
                raise HTTPException(status_code=500, detail="Failed to place order")

            await self.cart_collection.delete_many({"user_id": data["user_id"]})

            order_data["order_id"] = str(result.inserted_id)
            return order_data

        except Exception:
            raise HTTPException(status_code=500, detail="Error placing order")


    async def get_buyer_orders(self, data: dict):
        return await self.order_collection.find({"user_id": data["user_id"]}).to_list(length=None)

    async def get_order_details(self, data: dict):
        return await self.order_collection.find_one({"_id": ObjectId(data["order_id"]), "user_id": data["user_id"]})
