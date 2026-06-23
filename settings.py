from dotenv import load_dotenv
import os
import logging

logger = logging.getLogger(__name__)

load_dotenv(".env")

environment = os.getenv("ENVIRONMENT", "DEVELOPMENT").upper()

if environment == "DEVELOPMENT":
    load_dotenv(".env.development")
    logger.info(f"Environment loaded: {environment}!")
elif environment == "PRODUCTION":
    load_dotenv(".env.production")
    logger.info(f"Environment loaded: {environment}!")
else:
    logger.error(f"Invalid environment: {environment}!")
    raise ValueError(f"Invalid environment: {environment}!")


class Settings:
    ENVIRONMENT = environment
    DATABASE_URL = os.getenv("DATABASE_URL", "mysql+pymysql://root:123456@mysql:3306/pizzaria")
    JWT_TOKEN = os.getenv("JWT_TOKEN", "secret")
    ALGORITHM = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))
    REFRESH_TOKEN_EXPIRE_MINUTES = int(os.getenv("REFRESH_TOKEN_EXPIRE_MINUTES", "10080"))
    RUN_DATABASE_MIGRATIONS = os.getenv("RUN_DATABASE_MIGRATIONS", "False").lower() == "true"


settings = Settings()
