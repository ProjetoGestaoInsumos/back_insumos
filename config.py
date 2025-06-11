import os
from dotenv import load_dotenv
load_dotenv()

class Settings:
    DATABASE_URL: str = os.getenv("DATABASE_URL")
    SECRET_KEY: str = os.getenv("SECRET_KEY", "defaultsecret")
    
    EMAIL_ADDRESS: str = os.getenv("EMAIL_ADDRESS")
    EMAIL_PASSWORD: str = os.getenv("EMAIL_PASSWORD")

settings = Settings()