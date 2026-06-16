from fastapi import APIRouter, Depends, status
from dependencies.security_dependencies import verify_token
from dependencies.user_dependencies import get_user_service
from models.user import User
from schemas.response.auth.user_schema import ResponseUserSchema

user_router = APIRouter(prefix="/users", tags=["users"])

@user_router.get("/me", response_model=ResponseUserSchema)
async def get_me(user_service = Depends(get_user_service), user: User = Depends(verify_token)) -> ResponseUserSchema:
    return user_service.get_me(user.id)