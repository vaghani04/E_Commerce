from fastapi import HTTPException
from app.config.database import db_helper
from bson import ObjectId

class CartRepository:
    def __init__(self):
        self.cart_collection = db_helper.carts
        self.product_collection = db_helper.products

    async def add_to_cart(self, data: dict):
        try:
            product = await self.product_collection.find_one({"_id": data["product_id"]})
            if not product:
                raise HTTPException(status_code=404, detail="Product not found")

            await self.cart_collection.update_one(
                {"user_id": data["user_id"], "product_id": data["product_id"]},
                {"$inc": {"quantity": data["quantity"]}},
                upsert=True
            )

            cart_items = await self.cart_collection.find({"user_id": data["user_id"]}).to_list()

            cart_response_items = []
            total_price = 0

            for item in cart_items:
                product_details = await self.product_collection.find_one({"_id": item["product_id"]})
                if product_details:
                    subtotal = item["quantity"] * product_details["price"]
                    total_price += subtotal

                    cart_response_items.append({
                        "product_id": str(item["product_id"]),
                        "product_name": product_details["title"],
                        "product_price": product_details["price"],
                        "quantity": item["quantity"],
                        "subtotal": subtotal
                    })

            return {"items": cart_response_items, "total_price": total_price}

        except Exception:
            raise HTTPException(status_code=500, detail="Error adding to cart")
        
    async def remove_from_cart(self, data: dict):
        cart_item = await self.cart_collection.find_one({"user_id": data["user_id"], "product_id": data["product_id"]})
        if not cart_item:
            raise HTTPException(status_code=404, detail="Product not found in cart")

        await self.cart_collection.delete_one({"user_id": data["user_id"], "product_id": data["product_id"]})
        return {"message": "Product removed from cart successfully"}


    async def get_cart(self, data: dict):
        cart_items = await self.cart_collection.find({"user_id": data["user_id"]}).to_list(length=None)
        cart_response_items = []
        total_price = 0

        for item in cart_items:
            product_details = await self.product_collection.find_one({"_id": item["product_id"]});
            if product_details:
                subtotal = item["quantity"] * product_details["price"]
                total_price += subtotal
                cart_response_items.append({
                    "product_id": str(item["product_id"]),
                    "product_name": product_details["title"],
                    "product_price": product_details["price"],
                    "quantity": item["quantity"],
                    "subtotal": subtotal
                })

        return {"items": cart_response_items, "total_price": total_price}
