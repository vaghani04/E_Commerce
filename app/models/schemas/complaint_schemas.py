from pydantic import BaseModel
from typing import Literal
from bson import ObjectId

class ComplaintCreateSchema(BaseModel):
    order_id: str
    product_id: str
    issue: str

class ComplaintResponseSchema(BaseModel):
    user_id: str
    order_id: str
    product_id: str
    issue: str
    image_url: str
    status: Literal["open", "rejected"]
