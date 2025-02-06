from app.services.registration_service import RegistrationService, get_reg_service
from fastapi import Depends, HTTPException
from app.models.schemas.user_schemas import UserCreate

class TaskRegistration:
    
    def __init__(self, registration_service: RegistrationService = Depends(get_reg_service)):
        self.registration_service = registration_service
        
    async def task_registration(self, user: UserCreate):
        try:
            return await self.registration_service.create_user(user)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to create user: {str(e)}")
