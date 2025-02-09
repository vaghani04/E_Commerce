from fastapi import APIRouter, Depends, HTTPException
from app.models.schemas.user_schemas import UserResponse, UserRoleUpdate
from app.controllers.user_controllers import UserCon
from app.usecases.user_auth.verify_access_token import get_current_user
from typing import List

user_router = APIRouter(
    tags=["Users"]
)

@user_router.get("/users/me", response_model=UserResponse)
async def get_current_user_profile(user_controller: UserCon = Depends(), current_user: dict = Depends(get_current_user)):
    return await user_controller.get_current_user_details(current_user)

@user_router.get("/users", response_model=List[UserResponse])
async def get_all_users(user_controller: UserCon = Depends(), current_user: dict = Depends(get_current_user)):
    if current_user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Only admins can access this endpoint")
    return await user_controller.get_users()

@user_router.put("/users/{user_id}/role", response_model=UserRoleUpdate)
async def update_user_role(user_date: UserRoleUpdate, user_controller: UserCon = Depends(), current_user: dict = Depends(get_current_user)):
    if current_user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Only admins can update user roles")
    return await user_controller.update_user_role(user_date)