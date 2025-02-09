from fastapi import HTTPException
from app.config.database import db_helper
from app.models.schemas.user_schemas import UserResponse, UserRoleUpdate
from app.repositories.user_repo import UserRepo
from datetime import datetime

class UserService:
    def __init__(self):
        self.user_repo = UserRepo()
        self.collection = db_helper.users

    async def update_user_role(self, user_data: UserRoleUpdate):
        try:
            user = await self.user_repo.update_user_role(user_data.user_id, user_data.role)
            if not user:
                raise HTTPException(status_code=404, detail="User not found")
            return UserRoleUpdate(
                user_id=user["_id"],
                role=user["role"]
            )
        except Exception as e:
            if isinstance(e, HTTPException):
                raise e
            raise HTTPException(
                status_code=500,
                detail=f"Failed to update user role: {str(e)}"
            )
        
    async def get_specific_user(self, user_id: str):
        try:
            user = await self.user_repo.get_user_by_id(user_id)
            if not user:
                raise HTTPException(status_code=404, detail="User not found")
                
            return UserResponse(
                _id=str(user["_id"]),
                name=user["name"],
                email=user["email"],
                role=user["role"],
                created_at=user["created_at"],
                updated_at=user["updated_at"]
            )
                
        except Exception as e:
            if isinstance(e, HTTPException):
                raise e
            raise HTTPException(
                status_code=500, 
                detail=f"Failed to fetch user: {str(e)}"
            )

    async def get_all_users(self):
        try:
            users = await self.user_repo.get_all_users()
            
            if not users:
                return []

            user_responses = [
                UserResponse(
                    name=user["name"],
                    email=user["email"],
                    role=user["role"],
                    created_at=user["created_at"],
                    updated_at=user["updated_at"]
                    # created_at=datetime.fromisoformat(user["created_at"]) if isinstance(user["created_at"], str) else user["created_at"],
                    # updated_at=datetime.fromisoformat(user["updated_at"]) if isinstance(user["updated_at"], str) else user["updated_at"]
                ) for user in users
            ]
            
            return user_responses
            
        except Exception as e:
            raise HTTPException(
                status_code=500, 
                detail=f"Failed to fetch users: {str(e)}"
            )

def get_user_service():
    return UserService()