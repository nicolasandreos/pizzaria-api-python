import os

from fastapi import FastAPI
from passlib.context import CryptContext
from dotenv import load_dotenv
from fastapi.security import OAuth2PasswordBearer

load_dotenv()

BCRYPT_PASSWORD = os.getenv("BCRYPT_PASSWORD")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")) # minutes
REFRESH_TOKEN_EXPIRE_MINUTES = int(os.getenv("REFRESH_TOKEN_EXPIRE_MINUTES")) # days
ALGORITHM = os.getenv("ALGORITHM")
JWT_TOKEN = os.getenv("JWT_TOKEN")

app = FastAPI()

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_schema = OAuth2PasswordBearer(tokenUrl="auth/login")

from routes.auth_router import auth_router
from routes.order_router import order_router

app.include_router(auth_router)
app.include_router(order_router)

# Para rodar a aplicação, use o comando: uvicorn main:app --reload