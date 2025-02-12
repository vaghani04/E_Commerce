from pydantic_settings import BaseSettings
import os
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    MONGODB_URL: str = os.getenv("MONGODB_URL")
    DATABASE_NAME: str = os.getenv("DATABASE_NAME")
    SECRET_KEY: str = os.getenv("SECRET_KEY")
    ALGORITHM: str = os.getenv("ALGORITHM")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    GCP_BUCKET_NAME: str = os.getenv("GCP_BUCKET_NAME")
    COMPLAINT_FOLDER_NAME: str = os.getenv("COMPLAINT_FOLDER_NAME")
    SERVICE_ACC_JSON: str = os.getenv("SERVICE_ACC_JSON")

    class Config:
        env_file = ".env"

settings = Settings()