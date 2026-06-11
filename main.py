import os

from fastapi import FastAPI
from passlib.context import CryptContext
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv("BCRYPT_PASSWORD")

app = FastAPI()

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

from routes.auth_router import auth_router
from routes.order_router import order_router

app.include_router(auth_router)
app.include_router(order_router)

# Para rodar a aplicação, use o comando: uvicorn main:app --reload