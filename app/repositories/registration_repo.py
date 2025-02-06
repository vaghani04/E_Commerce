from app.config.database import db_helper
from app.models.schemas.user_schemas import UserCreate

class UserRegistrationRepo:
    def __init__(self):
        self.collection = db_helper.users

    async def add_user(self, user_data: UserCreate):
        result = await self.collection.insert_one(user_data)
        return result
    
    async def get_user(self, _id: dict):
        user = await self.collection.find_one(_id)
        return user
    
def get_user_reg_repo():
    return UserRegistrationRepo()