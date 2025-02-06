from app.config.database import mongo_db_obj
from passlib.context import CryptContext
from app.models.schemas import user_schemas
from app.models.domain import registration_domain
from app.utils.helper import user_helper
from app.repositories.registration_repo import UserRegistrationRepo
from fastapi import Depends


class RegistrationService:
    
    def __init__(self):
        self.pwd_context = CryptContext(schemes = ['bcrypt'], deprecated = 'auto')
        self.user_reg_repo = UserRegistrationRepo()
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
    
    async def create_user(self, user: user_schemas.User):
        hashed_password = self.pwd_context.hash(user.password)
        
        obj = registration_domain.User(name = user.name, email = user.email, password = user.password, role = user.role)
        user_data = obj.to_dict()

        user_data['password'] = hashed_password

        result = await self.user_reg_repo.add_user(user_data = user_data)
        signed_user = await self.user_reg_repo.get_user(_id = {'_id': result.inserted_id})
        return user_helper(signed_user)
    
def get_reg_service() -> RegistrationService:
    return RegistrationService()