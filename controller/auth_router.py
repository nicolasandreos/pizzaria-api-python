from fastapi import APIRouter, Depends, status
from dependencies.admin_dependencies import get_admin_user
from models import User

# dependencies
from dependencies.jwt_dependencies import get_jwt_service
from dependencies.security_dependencies import verify_token
from dependencies.auth_dependencies import get_auth_service

# schemas
from schemas.request.auth.create_user_schema import RequestCreateUserSchema
from schemas.request.auth.login_user_schema import RequestLoginSchema
from schemas.response.auth.get_user_schema import ResponseGetUserSchema
from schemas.response.auth.login_schema import ResponseLoginSchema
from schemas.response.auth.access_token_schema import ResponseAccessTokenSchema
from fastapi.security import OAuth2PasswordRequestForm
from schemas.response.auth.create_user_schema import ResponseCreateUserSchema

# services
from services.auth_service import AuthService
from services.jwt_service import JwtService

auth_router = APIRouter(prefix="/auth", tags=["auth"])


@auth_router.post("/login", response_model=ResponseLoginSchema, status_code=status.HTTP_200_OK)
async def login(login_schema: RequestLoginSchema, auth_service: AuthService = Depends(get_auth_service)) -> ResponseLoginSchema:
    return auth_service.login(login_schema)


@auth_router.get("/me", response_model=ResponseGetUserSchema, status_code=status.HTTP_200_OK)
async def get_user(user: User = Depends(verify_token)) -> ResponseGetUserSchema:
    return ResponseGetUserSchema(name=user.name, email=user.email, created_at=user.created_at, active=user.active, admin=user.admin)
    

@auth_router.post("/login-form-docs", response_model=ResponseLoginSchema, status_code=status.HTTP_200_OK)
async def login_form_docs(form_data: OAuth2PasswordRequestForm = Depends(), auth_service: AuthService = Depends(get_auth_service)) -> ResponseLoginSchema:
    return auth_service.login_form_docs(form_data)


@auth_router.post("/register", response_model=ResponseCreateUserSchema, status_code=status.HTTP_201_CREATED)
async def create_account(user_schema: RequestCreateUserSchema, auth_service: AuthService = Depends(get_auth_service)) -> ResponseCreateUserSchema:
    return auth_service.register(user_schema, is_admin=False)


@auth_router.post("/register-admin", response_model=ResponseCreateUserSchema, status_code=status.HTTP_201_CREATED)
async def create_admin(user_schema: RequestCreateUserSchema, auth_service: AuthService = Depends(get_auth_service), admin_user: User = Depends(get_admin_user)) -> ResponseCreateUserSchema:
    return auth_service.register(user_schema, is_admin=True)


@auth_router.post("/refresh-access-token", response_model=ResponseAccessTokenSchema, status_code=status.HTTP_200_OK)
async def refresh_access_token(user: User = Depends(verify_token), jwt_service: JwtService = Depends(get_jwt_service)) -> ResponseAccessTokenSchema:
    return ResponseAccessTokenSchema(access_token=jwt_service.create_access_token(user.id), token_type="Bearer")
