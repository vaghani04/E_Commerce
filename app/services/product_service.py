from fastapi import HTTPException
from app.config.database import db_helper
from app.models.schemas.product_schemas import ProductCreate, ProductResponse
from app.repositories.product_repo import ProductRepo
from app.models.domain import product_domain
from typing import List
from datetime import datetime, timezone
from bson import ObjectId

class ProductService:
    def __init__(self):
        self.product_repo = ProductRepo()
        self.collection = db_helper.products

    async def create_product(self, product: ProductCreate, current_user: dict):
        try:
            if current_user['role'] != "seller":
                raise HTTPException(status_code=403, detail="Only sellers can create products")

            obj = product_domain.Product(
                title=product.title,
                description=product.description,
                category=product.category,
                price=product.price,
                rating=product.rating,
                brand=product.brand
            )
            product_data = obj.to_dict()
            product_data["seller_id"] = current_user["sub"]
            result = await self.product_repo.add_product(product_data)
            if not result:
                raise HTTPException(status_code=500, detail="Error inserting product into the database")

            return await self.product_repo.get_product({"_id": result.inserted_id})
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to create product: {str(e)}")

    async def get_all_products(self) -> List[ProductResponse]:
        try:
            products = await self.product_repo.get_all_products()
            
            if not products:
                return []

            product_responses = [
                ProductResponse(
                    title=product["title"],
                    description=product["description"],
                    category=product["category"],
                    price=product["price"],
                    rating=product["rating"],
                    brand=product["brand"],
                    created_at=datetime.fromisoformat(product["created_at"]) if isinstance(product["created_at"], str) else product["created_at"],
                    updated_at=datetime.fromisoformat(product["updated_at"]) if isinstance(product["updated_at"], str) else product["updated_at"]
                ) for product in products
            ]
            
            return product_responses
            
        except Exception as e:
            raise HTTPException(
                status_code=500, 
                detail=f"Failed to fetch products: {str(e)}"
            )
        
    async def get_specific_product(self, product_id: str):
        try:
            product = await self.product_repo.get_product(product_id)
            
            if not product:
                raise HTTPException(status_code=404, detail="Product not found")
                
            return ProductResponse.model_validate(product)
            
        except Exception as e:
            if isinstance(e, HTTPException):
                raise e
            raise HTTPException(status_code=500, detail=f"Failed to fetch product: {str(e)}")

    async def update_product(self, product_id: str, product: ProductCreate):
        try:
            existing_product = await self.product_repo.get_product(product_id)
            if not existing_product:
                raise HTTPException(status_code=404, detail="Product not found")

            update_data = {
                "title": product.title,
                "description": product.description,
                "category": product.category,
                "price": product.price,
                "rating": product.rating,
                "brand": product.brand,
                "updated_at": datetime.now(timezone.utc)
            }

            updated_product = await self.product_repo.update_product(
                product_id=ObjectId(product_id),
                update_data=update_data
            )

            if not updated_product:
                raise HTTPException(status_code=500, detail="Failed to update product")
            return updated_product
        
        except Exception as e:
            if isinstance(e, HTTPException):
                raise e
            raise HTTPException(status_code=500, detail=f"Failed to update product: {str(e)}")

    async def delete_product(self, product_id: str):
        try:
            product = await self.product_repo.get_product(product_id)
            if not product:
                raise HTTPException(status_code=404, detail="Product not found")

            delete_result = await self.product_repo.delete_product(product_id)
            print(delete_result)
            if not delete_result or delete_result.deleted_count == 0:
                raise HTTPException(status_code=500, detail="Failed to delete product")
            
            return {"message": "Product deleted successfully"}
        
        except Exception as e:
            if isinstance(e, HTTPException):
                raise e
            raise HTTPException(status_code=500, detail=f"Failed to delete product: {str(e)}")
    
def get_product_service() -> ProductService:
    return ProductService()