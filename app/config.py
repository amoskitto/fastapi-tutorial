from pydantic_settings import BaseSettings
from dotenv import load_dotenv
import os

# Load .env file from the project root
load_dotenv(override=True)

class Settings(BaseSettings):
    database_hostname: str
    database_port: str
    database_password: str
    database_name: str
    database_username: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()
