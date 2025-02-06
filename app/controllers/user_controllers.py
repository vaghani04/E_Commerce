from fastapi import HTTPException, Depends
from app.usecases.users import fetch_users_usecase, update_users_usecase
from app.models.schemas.user_schemas import UserRoleUpdate
from typing import List

class UserCon:

    def __init__(self, get_user_usecase: fetch_users_usecase.TaskUserFetch = Depends(), update_user_usecase: update_users_usecase.TaskUserUpdate = Depends()):
        self.update_user_usecase = update_user_usecase
        self.user_fetch_usecase = get_user_usecase

    async def get_users(self):
        return await self.user_fetch_usecase.task_get_users()

    async def get_current_user_details(self, current_user: dict):
        return await self.user_fetch_usecase.task_get_specific_user(current_user["sub"])

    async def update_user_role(self, user_data: UserRoleUpdate):
        return await self.update_user_usecase.task_update_user_role(user_data)