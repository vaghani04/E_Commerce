from fastapi import Depends
from app.usecases.products import upload_product_usecase, fetch_products_usecase, delete_product_usecase
from app.models.schemas.product_schemas import ProductCreate

class ProductCon:
    def __init__(self, product_usecase: upload_product_usecase.TaskProductUpload = Depends(), product_fetch_usecase: fetch_products_usecase.TaskProductFetch = Depends(), product_delete_usecase: delete_product_usecase.TaskProductDelete = Depends()):
        self.product_usecase = product_usecase
        self.product_fetch_usecase = product_fetch_usecase
        self.product_delete_usecase = product_delete_usecase

    async def upload_product(self, product: ProductCreate):
        return await self.product_usecase.task_upload_product(product)
    
    async def get_products(self):
        return await self.product_fetch_usecase.task_get_products()

    async def get_specific_product(self, product_id: str):
        return await self.product_fetch_usecase.task_get_specific_product(product_id = product_id)
    
    async def update_product(self, product_id: str, product: ProductCreate):
        # print(str(product_id))
        return await self.product_usecase.task_update_product(product_id, product)
    
    async def delete_product(self, product_id: str):
        print(product_id)
        return await self.product_delete_usecase.task_delete_product(product_id)