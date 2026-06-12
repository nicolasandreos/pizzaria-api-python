from fastapi import APIRouter, Depends
from models import User

# dependencies
from dependencies.jwt_dependencies import get_jwt_service
from dependencies.security_dependencies import verify_token
from dependencies.auth_dependencies import get_auth_service

# schemas
from schemas.request.auth.create_user_schema import RequestCreateUserSchema
from schemas.request.auth.login_user_schema import RequestLoginSchema
from schemas.response.auth.login_schema import ResponseLoginSchema
from schemas.response.auth.access_token_schema import ResponseAccessTokenSchema
from fastapi.security import OAuth2PasswordRequestForm
from schemas.response.auth.create_user_schema import ResponseCreateUserSchema

# services
from services.auth_service import AuthService
from services.jwt_service import JwtService

auth_router = APIRouter(prefix="/auth", tags=["auth"])

@auth_router.post("/login", response_model=ResponseLoginSchema)
async def login(login_schema: RequestLoginSchema, auth_service: AuthService = Depends(get_auth_service)) -> ResponseLoginSchema:
    return auth_service.login(login_schema)


@auth_router.post("/login-form-docs", response_model=ResponseLoginSchema)
async def login_form_docs(form_data: OAuth2PasswordRequestForm = Depends(), auth_service: AuthService = Depends(get_auth_service)) -> ResponseLoginSchema:
    return auth_service.login_form_docs(form_data)


@auth_router.post("/register")
async def create_account(user_schema: RequestCreateUserSchema, auth_service: AuthService = Depends(get_auth_service)) -> ResponseCreateUserSchema:
    return auth_service.register(user_schema)


@auth_router.get("/refresh-access-token")
async def refresh_access_token(user: User = Depends(verify_token), jwt_service: JwtService = Depends(get_jwt_service)) -> ResponseAccessTokenSchema:
    return jwt_service.create_access_token(user.id)
