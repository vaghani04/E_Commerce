from app.config.database import db_helper
from bson import ObjectId
from fastapi import HTTPException, status

class UserRepo:
    def __init__(self):
        self.collection = db_helper.users

    async def get_user_by_id(self, user_id: str):
        user = await self.collection.find_one({"_id": ObjectId(user_id)})
        if user:
            user["_id"] = str(user["_id"])
        return user

    async def get_all_users(self):
        users = []
        async for user in self.collection.find():
            user["_id"] = str(user["_id"])
            users.append(user)
        if users:
            return users
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='No users found.')

    async def update_user_role(self, user_id: str, role: str):
        try:
            result = await self.collection.find_one_and_update(
                {"_id": ObjectId(user_id)},
                {"$set": {"role": role}},
                return_document=True
            )
            if result:
                result["_id"] = str(result["_id"])
            return result
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Error updating user role: {str(e)}"
            )