from app.services.user_service import UserService, get_user_service
from fastapi import Depends
from app.models.schemas.user_schemas import UserRoleUpdate

class TaskUserFetch:
    def __init__(self, user_service: UserService = Depends(get_user_service)):
        self.user_service = user_service

    async def task_get_users(self):
        return await self.user_service.get_all_users()

    async def task_get_specific_user(self, user_id: str):
        return await self.user_service.get_specific_user(user_id)