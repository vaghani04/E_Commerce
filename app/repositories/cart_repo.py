# # app/repositories/cart_repo.py
# from fastapi import HTTPException
# from app.config.database import db_helper
# from bson import ObjectId
# from typing import List, Dict, Any
# from datetime import datetime, timezone

# class CartRepository:
#     def __init__(self):
#         self.cart_collection = db_helper.carts
#         self.product_collection = db_helper.products
#         self.order_collection = db_helper.orders

#     async def add_to_cart(self, user_id: str, product_id: str, quantity: int = 1):
#         try:
#             # Validate product exists
#             product = await self.product_collection.find_one({"_id": ObjectId(product_id)})
#             if not product:
#                 raise HTTPException(status_code=404, detail="Product not found")

#             # Upsert cart item
#             result = await self.cart_collection.update_one(
#                 {"user_id": user_id, "product_id": product_id},
#                 {"$inc": {"quantity": quantity}},
#                 upsert=True
#             )
#             return result
#         except Exception as e:
#             raise HTTPException(status_code=500, detail=f"Error adding to cart: {str(e)}")

#     async def remove_from_cart(self, user_id: str, product_id: str):
#         try:
#             result = await self.cart_collection.delete_one({
#                 "user_id": user_id, 
#                 "product_id": product_id
#             })
#             return result.deleted_count > 0
#         except Exception as e:
#             raise HTTPException(status_code=500, detail=f"Error removing from cart: {str(e)}")

#     async def get_cart(self, user_id: str):
#         try:
#             cart_items = await self.cart_collection.find({"user_id": user_id}).to_list(length=None)
            
#             # Enrich cart items with product details
#             enriched_items = []
#             total_price = 0
#             for item in cart_items:
#                 product = await self.product_collection.find_one({"_id": ObjectId(item['product_id'])})
#                 if product:
#                     item_price = product.get('price', 0)
#                     subtotal = item_price * item['quantity']
#                     enriched_item = {
#                         "product_id": str(item['product_id']),
#                         "product_name": product.get('name', 'Unknown Product'),
#                         "quantity": item['quantity'],
#                         "product_price": item_price,
#                         "subtotal": subtotal
#                     }
#                     enriched_items.append(enriched_item)
#                     total_price += subtotal

#             return {"items": enriched_items, "total_price": total_price}
#         except Exception as e:
#             raise HTTPException(status_code=500, detail=f"Error fetching cart: {str(e)}")

#     async def create_order(self, user_id: str):
#         try:
#             # Get cart items
#             cart = await self.get_cart(user_id)
            
#             if not cart['items']:
#                 raise HTTPException(status_code=400, detail="Cart is empty")

#             # Create order document
#             order = {
#                 "user_id": user_id,
#                 "items": cart['items'],
#                 "total_price": cart['total_price'],
#                 "created_at": datetime.now(timezone.utc),
#                 "status": "pending"
#             }

#             # Insert order
#             result = await self.order_collection.insert_one(order)
            
#             # Clear cart after order creation
#             await self.cart_collection.delete_many({"user_id": user_id})

#             return str(result.inserted_id)
#         except Exception as e:
#             raise HTTPException(status_code=500, detail=f"Error creating order: {str(e)}")

#     async def get_orders(self, user_id: str):
#         try:
#             orders = await self.order_collection.find({"user_id": user_id}).to_list(length=None)
#             return [
#                 {
#                     "order_id": str(order['_id']),
#                     "user_id": order['user_id'],
#                     "items": order['items'],
#                     "total_price": order['total_price'],
#                     "created_at": order['created_at'],
#                     "status": order.get('status', 'pending')
#                 } for order in orders
#             ]
#         except Exception as e:
#             raise HTTPException(status_code=500, detail=f"Error fetching orders: {str(e)}")

#     async def get_order_details(self, user_id: str, order_id: str):
#         try:
#             order = await self.order_collection.find_one({
#                 "_id": ObjectId(order_id), 
#                 "user_id": user_id
#             })
            
#             if not order:
#                 raise HTTPException(status_code=404, detail="Order not found")

#             return {
#                 "order_id": str(order['_id']),
#                 "user_id": order['user_id'],
#                 "items": order['items'],
#                 "total_price": order['total_price'],
#                 "created_at": order['created_at'],
#                 "status": order.get('status', 'pending')
#             }
#         except Exception as e:
#             raise HTTPException(status_code=500, detail=f"Error fetching order details: {str(e)}")

# def get_cart_repo() -> CartRepository:
#     return CartRepository()

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
