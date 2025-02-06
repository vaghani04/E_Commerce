from app.config.database import db_helper
from fastapi import Depends
from datetime import datetime, timedelta
from app.config.settings import settings
import jwt


class LoginService:
    
    def __init__(self):
        self.collection = db_helper.users
        
    async def get_user_by_name(self, name: str):
        get_user_pipeline = [
            {
                '$match': {
                    'name': name
                }
            }
        ]
        cursor = self.collection.aggregate(pipeline=get_user_pipeline)
        async for document in cursor:
            if document:
                return document
        return {}
    
    def create_access_token(self, data: dict):
        to_encode = data.copy()
        expire = datetime.now() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, settings.ALGORITHM)
        
        return encoded_jwt
    
def get_login_service() -> LoginService:
    return LoginService()