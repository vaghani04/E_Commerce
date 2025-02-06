from fastapi import Depends
from app.models.schemas.user_schemas import Login
from app.usecases.user_auth.login_usecase import TaskLoginUser
class LoginCon:

    def __init__(self, login_user: TaskLoginUser = Depends()):
        self.login_user = login_user

    async def do_login(self, user_info: Login):
        return await self.login_user.task_login(user_info = user_info)