import os

from fastapi import FastAPI
from dotenv import load_dotenv
from fastapi.security import OAuth2PasswordBearer
from fastapi.exceptions import RequestValidationError

# Exceptions
from exceptions.base_exception import ApplicationException
from handlers.exception_handlers import api_exception_handler, pydantic_request_validation_exception_handler

load_dotenv()

ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")) # minutes
REFRESH_TOKEN_EXPIRE_MINUTES = int(os.getenv("REFRESH_TOKEN_EXPIRE_MINUTES")) # days
ALGORITHM = os.getenv("ALGORITHM")
JWT_TOKEN = os.getenv("JWT_TOKEN")

app = FastAPI()

# Exception handlers
app.add_exception_handler(ApplicationException, api_exception_handler)
app.add_exception_handler(RequestValidationError, pydantic_request_validation_exception_handler)

oauth2_schema = OAuth2PasswordBearer(tokenUrl="auth/login-form-docs", auto_error=False)

from controller.auth_router import auth_router
from controller.order_router import order_router
from controller.product_router import product_router

app.include_router(auth_router)
app.include_router(order_router)
app.include_router(product_router)

# Para rodar a aplicação, use o comando: uvicorn main:app --reload