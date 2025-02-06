from fastapi import APIRouter, Depends, status
from app.models.schemas.product_schemas import ProductCreate, ProductResponse
from app.controllers.product_controller import ProductCon

product_router = APIRouter(
    tags = ["Products"]
)

@product_router.post("/products", status_code=status.HTTP_201_CREATED)
async def upload_product(product_data: ProductCreate, product_controller: ProductCon = Depends()):
    return await product_controller.upload_product(product = product_data)

@product_router.get("/products", status_code=status.HTTP_200_OK)
async def get_products(product_controller: ProductCon = Depends()):
    return await product_controller.get_products()

@product_router.get("/products/{product_id}", status_code = status.HTTP_200_OK)
async def get_product(product_id: str, product_controller: ProductCon = Depends()):
    return await product_controller.get_specific_product(product_id = product_id)

@product_router.put("/products/{product_id}", status_code=status.HTTP_200_OK)
async def update_product(product_id: str, product: ProductCreate, product_controller: ProductCon = Depends()):
   return await product_controller.update_product(product_id=product_id, product=product)

@product_router.delete("/products/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(product_id: str, product_controller: ProductCon = Depends()):
   return await product_controller.delete_product(product_id=product_id)