from app.config.database import db_helper
from passlib.context import CryptContext
from app.models.schemas.user_schemas import UserCreate
from app.models.domain import registration_domain
from app.utils.helper import user_helper
from app.repositories.registration_repo import UserRegistrationRepo
from datetime import datetime, timezone

class RegistrationService:
    
    def __init__(self):
        self.pwd_context = CryptContext(schemes = ['bcrypt'], deprecated = 'auto')
        self.user_reg_repo = UserRegistrationRepo()
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
    
    async def create_user(self, user: UserCreate):
        hashed_password = self.pwd_context.hash(user.password)

        domain_user = registration_domain.User(
            name=user.name,
            email=user.email,
            password=user.password,
            role=user.role,
        )

        user_data = domain_user.to_dict()
        user_data["password"] = hashed_password
        user_data["created_at"] = datetime.now(timezone.utc)
        user_data["updated_at"] = datetime.now(timezone.utc)
        print(user_data)

        result = await self.user_reg_repo.add_user(user_data=user_data)
        signed_user = await self.user_reg_repo.get_user(_id={'_id': result.inserted_id})
        return user_helper(signed_user)
    
def get_reg_service() -> RegistrationService:
    return RegistrationService()