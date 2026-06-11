from sqlalchemy.orm import Session
from dependencies import get_session
from repository.user_repository import UserRepository
from services.auth_service import AuthService
from services.password_service import PasswordService
from services.jwt_service import JwtService
from fastapi import Depends

def get_auth_service(session: Session = Depends(get_session)):
    
    repository = UserRepository(session)
    password_service = PasswordService()
    jwt_service = JwtService()

    return AuthService(repository, password_service, jwt_service)