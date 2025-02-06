from fastapi import APIRouter, Depends, status, HTTPException
from app.models.schemas.product_schemas import ProductCreate, ProductResponse
from app.controllers.product_controller import ProductCon
from typing import List
from app.usecases.user_auth.verify_access_token import get_current_user

product_router = APIRouter(
    tags = ["Products"]
)

@product_router.post("/products", status_code=status.HTTP_201_CREATED, response_model=ProductResponse)
async def upload_product(product_data: ProductCreate, product_controller: ProductCon = Depends(), current_user: dict = Depends(get_current_user)):
    if current_user["role"] != "seller":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only sellers can add products")
    return await product_controller.upload_product(product=product_data, current_user=current_user)

@product_router.get("/products", status_code=status.HTTP_200_OK, response_model=List[ProductResponse])
async def get_products(product_controller: ProductCon = Depends()):
    return await product_controller.get_products()

@product_router.get("/products/{product_id}", status_code=status.HTTP_200_OK, response_model=ProductResponse)
async def get_product(product_id: str, product_controller: ProductCon = Depends()):
    return await product_controller.get_specific_product(product_id=product_id)

@product_router.put("/products/{product_id}", status_code=status.HTTP_200_OK, response_model=ProductResponse)
async def update_product(product_id: str, product: ProductCreate, product_controller: ProductCon = Depends(), current_user: dict = Depends(get_current_user)):
    existing_product = await product_controller.get_specific_product(product_id=product_id)
    if existing_product.seller_id != current_user["sub"]:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only the seller who uploaded the product can update it")
    return await product_controller.update_product(product_id=product_id, product=product)

@product_router.delete("/products/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(product_id: str, product_controller: ProductCon = Depends(), current_user: dict = Depends(get_current_user)):
    existing_product = await product_controller.get_specific_product(product_id=product_id)
    if existing_product.seller_id != current_user["sub"]:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only the seller who uploaded the product can delete it")
    return await product_controller.delete_product(product_id=product_id)