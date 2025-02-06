from app.services.user_service import UserService, get_user_service
from fastapi import Depends
from app.models.schemas.user_schemas import UserRoleUpdate

class TaskUserUpdate:
    def __init__(self, user_service: UserService = Depends(get_user_service)):
        self.user_service = user_service

    async def task_update_user_role(self, user_data: UserRoleUpdate):
        return await self.user_service.update_user_role(user_data)
