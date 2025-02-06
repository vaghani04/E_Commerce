from fastapi import Depends
from app.models.schemas.user_schemas import UserCreate
from app.usecases.user_auth.registration_usecase import TaskRegistration

class RegistrationCon:
    
    def __init__(self, register_user: TaskRegistration = Depends()):
        self.register_user = register_user
    
    async def do_registration(self, user = UserCreate):
        return await self.register_user.task_registration(user = user)