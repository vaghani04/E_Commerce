from app.services.product_service import ProductService, get_product_service
from fastapi import Depends

class TaskProductFetch:
    def __init__(self, product_service: ProductService = Depends(get_product_service)):
        self.product_service = product_service

    async def task_get_products(self):
        return await self.product_service.get_all_products()
    
    async def task_get_specific_product(self, product_id: str):
        return await self.product_service.get_specific_product(product_id = product_id)