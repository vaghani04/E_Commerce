# app/models/schemas/cart_schemas.py
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class CartItemCreate(BaseModel):
    product_id: str
    quantity: int = Field(default=1, gt=0)

class CartItem(CartItemCreate):
    product_name: str
    product_price: float
    subtotal: float

class CartResponse(BaseModel):
    items: List[CartItem]
    total_price: float

class OrderCreate(BaseModel):
    cart_items: List[CartItemCreate]

class OrderItem(BaseModel):
    product_id: str
    product_name: str
    quantity: int
    price: float

class OrderResponse(BaseModel):
    order_id: str
    user_id: str
    items: List[OrderItem]
    total_price: float
    created_at: datetime
    status: str = "pending"

class OrderDetailResponse(OrderResponse):
    shipping_address: Optional[str] = None
    payment_method: Optional[str] = None