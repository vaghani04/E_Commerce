from app.services.product_service import ProductService, get_product_service
from fastapi import Depends

class TaskProductDelete:
    def __init__(self, product_service: ProductService = Depends(get_product_service)):
        self.product_service = product_service

    async def task_delete_product(self, product_id: str):
        print(f'task: {product_id}')
        return await self.product_service.delete_product(product_id=product_id)