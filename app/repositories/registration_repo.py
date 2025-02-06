from app.config.database import mongo_db_obj
from app.models.schemas import user_schemas

class UserRegistrationRepo:
    def __init__(self):
        self.collection = mongo_db_obj.user_collection

    async def add_user(self, user_data: user_schemas.User):
        result = await self.collection.insert_one(user_data)
        return result
    
    async def get_user(self, _id: dict):
        user = await self.collection.find_one(_id)
        return user
    
def get_user_reg_repo() -> UserRegistrationRepo:
    return UserRegistrationRepo()