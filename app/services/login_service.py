from app.config.database import mongo_db_obj
from fastapi import Depends
from datetime import datetime, timedelta
from app.config.settings import Config
import jwt


class LoginService:
    
    def __init__(self):
        self.collection = mongo_db_obj.user_collection
        
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

        expire = datetime.now() + timedelta(minutes=Config.ACCESS_TOKEN_EXPIRE_MINUTES)

        to_encode.update({"exp": expire})

        encoded_jwt = jwt.encode(to_encode, Config.SECRET_KEY, Config.ALGORITHM)
        
        return encoded_jwt
    
def get_login_service() -> LoginService:
    return LoginService()