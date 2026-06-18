from dotenv import load_dotenv
import os

load_dotenv(".env")
environment = os.getenv("ENVIRONMENT", "development")

if environment == "development":
    load_dotenv(".env.development")
elif environment == "production":
    load_dotenv(".env.production")
else:
    raise ValueError(f"Invalid environment: {environment}")


class Settings:
    ENVIRONMENT = environment
    DATABASE_URL = os.getenv("DATABASE_URL")
    JWT_TOKEN = os.getenv("JWT_TOKEN")
    ALGORITHM = os.getenv("ALGORITHM")
    ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))
    REFRESH_TOKEN_EXPIRE_MINUTES = int(os.getenv("REFRESH_TOKEN_EXPIRE_MINUTES", "10080"))


settings = Settings()
