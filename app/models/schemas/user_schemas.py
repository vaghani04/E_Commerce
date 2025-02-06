from pydantic import BaseModel, EmailStr
from typing import Literal
from datetime import datetime

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str
    role: Literal['admin', 'buyer', 'seller']
    
class UserResponse(BaseModel):
    _id: str
    name: str
    email: EmailStr
    role: str
    created_at: datetime
    updated_at: datetime

class Login(BaseModel):
    name: str
    password: str
    
class AccessToken(BaseModel):
    access_token: str
    token_type: str