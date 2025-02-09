from fastapi import Depends, HTTPException
from app.services.product_service import ProductService, get_product_service
from app.models.schemas.product_schemas import ProductCreate

class TaskProductUpload:
    def __init__(self, product_service: ProductService = Depends(get_product_service)):
        self.product_service = product_service

    async def task_upload_product(self, product: ProductCreate, current_user: dict):
        try:
            return await self.product_service.create_product(product, current_user)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to upload product: {str(e)}")
             
    
    async def task_update_product(self, product_id: str, product: ProductCreate, current_user: dict):
        try:
            return await self.product_service.update_product(product_id, product, current_user)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to upload product: {str(e)}")
