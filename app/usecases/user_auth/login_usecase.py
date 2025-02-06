from app.services.login_service import LoginService, get_login_service
from fastapi import Depends, HTTPException
from app.models.schemas.user_schemas import Login
from app.utils.utility import check_password

class TaskLoginUser:
    
    def __init__(self, login_service: LoginService = Depends(get_login_service)):
        self.login_service = login_service
        
    async def task_login(self, user_info: Login):
        user = await self.login_service.get_user_by_name(name=user_info.name)

        if not user:
            raise HTTPException(status_code=401, detail='Invalid credentials')
        if not await check_password(plain_password=user_info.password, hashed_password=user['password']):
            raise HTTPException(status_code=401, detail="Invalid credentials")
        
        access_token = self.login_service.create_access_token({"sub": str(user["_id"]), "role": user["role"]})

        return {
            'access_token': access_token,
            'token_type': 'bearer'
        }
