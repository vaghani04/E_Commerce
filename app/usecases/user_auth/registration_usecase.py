from app.services.registration_service import RegistrationService, get_reg_service
from fastapi import Depends, HTTPException, status
from app.models.schemas.user_schemas import UserCreate

class TaskRegistration:
    
    def __init__(self, registration_service: RegistrationService = Depends(get_reg_service)):
        self.registration_service = registration_service
        
    async def task_registration(self, user: UserCreate):
        # is_exists = await self.registration_service.get_user_by_name(name = user.name)
        
        # if is_exists:
        #     raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='User already exists.')
        
        # else:
        #     return await self.registration_service.create_user(user = user)

        try:
            return await self.registration_service.create_user(user)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to create user: {str(e)}")
             