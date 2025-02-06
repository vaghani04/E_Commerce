from fastapi import APIRouter, Depends, status
from app.models.schemas.user_schemas import User, Login, AccessToken
from app.controllers import registration_controller, login_controller

auth_router = APIRouter()

@auth_router.post('/auth/register')
async def register_user(user_data: User, registration_controller: registration_controller.RegistrationCon = Depends()):
    return await registration_controller.do_registration(user = user_data)

@auth_router.post('/auth/login', status_code = status.HTTP_202_ACCEPTED, response_model = AccessToken)
async def login_user(user_info: Login, login_controller: login_controller.LoginCon = Depends()):
    return await login_controller.do_login(user_info = user_info)