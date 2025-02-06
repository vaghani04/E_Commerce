from pydantic import BaseModel, EmailStr
from typing import Literal

class User(BaseModel):
    model_config = {
        'extra' : 'ignore'
    }
    
    name: str
    email: EmailStr
    password: str
    role: Literal['admin', 'buyer', 'seller']
    
class Login(BaseModel):
    name: str
    password: str
    
class AccessToken(BaseModel):
    access_token: str
    token_type: str