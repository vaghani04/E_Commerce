from passlib.context import CryptContext

async def check_password(plain_password, hashed_password):
    pwd_context = CryptContext(schemes = ['bcrypt'], deprecated = 'auto')
    return pwd_context.verify(plain_password, hashed_password)