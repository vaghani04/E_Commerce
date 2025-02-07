from pydantic import BaseModel, Field
from typing import List
from datetime import datetime

class OrderItemSchema(BaseModel):
    product_id: str
    product_name: str
    product_price: float
    quantity: int
    subtotal: float

class OrderCreateSchema(BaseModel):
    user_id: str
    items: List[OrderItemSchema]
    total_price: float

class OrderResponseSchema(BaseModel):
    order_id: str
    user_id: str
    items: List[OrderItemSchema]
    total_price: float
    status: str
    created_at: datetime
