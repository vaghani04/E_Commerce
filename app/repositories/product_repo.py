from app.config.database import db_helper
from bson import ObjectId
from fastapi import HTTPException, status

class ProductRepo:
    def __init__(self):
        self.collection = db_helper.products

    async def add_product(self, product_data: dict):
        result = await self.collection.insert_one(product_data)
        print(product_data)
        return result
    
    async def get_product(self, product_id: str):
        product = await self.collection.find_one(product_id)
        if product:
            product["_id"] = str(product["_id"])
        return product
        
    async def get_all_products(self):
        products = []
        async for product in self.collection.find():
            product["_id"] = str(product["_id"])
            products.append(product)
        if products:
            return products
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = 'no products are there.')

    async def update_product(self, product_id: str, update_data: dict):
        try:
            result = await self.collection.find_one_and_update(
                {"_id": str(product_id)},
                {"$set": update_data},
                return_document=True  # This returns the updated document
            )
            return result
        except Exception as e:
            return None
        
    async def delete_product(self, product_id: str):
        try:
            result = await self.collection.delete_one({"_id": ObjectId(product_id)})
            return result
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Error deleting product: {str(e)}"
            )