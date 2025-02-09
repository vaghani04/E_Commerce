from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ProductCreate(BaseModel):
    title: str
    description: str
    category: str
    price: float
    brand: str
    rating: Optional[float] = 0.0

class ProductResponse(BaseModel):
    title: str
    seller_id: str
    description: str
    category: str
    price: float
    brand: str
    rating: float
    created_at: datetime
    updated_at: datetime