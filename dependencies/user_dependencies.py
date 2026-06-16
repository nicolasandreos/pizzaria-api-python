from dependencies.session_dependencies import get_session
from repositories.user_repository import UserRepository
from services.user_service import UserService
from fastapi import Depends
from sqlalchemy.orm import Session


def get_user_service(session: Session = Depends(get_session)) -> UserService:
    user_repository = UserRepository(session)
    return UserService(user_repository)
