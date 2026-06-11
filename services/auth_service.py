from repository.user_repository import UserRepository
from schemas.request.auth.create_user_schema import RequestCreateUserSchema
from schemas.request.auth.login_user_schema import RequestLoginSchema
from schemas.response.auth.login_schema import ResponseLoginSchema
from fastapi import HTTPException
from services.password_service import PasswordService
from models import User
from services.jwt_service import JwtService

class AuthService:

    def __init__(self, user_repository: UserRepository, password_service: PasswordService, jwt_service: JwtService):
        self._repository = user_repository
        self._password_service = password_service
        self._jwt_service = jwt_service

    def register(self, register_schema: RequestCreateUserSchema):
        user = self._repository.get_by_email(register_schema.email)

        if user:
            raise HTTPException(status_code=409, detail="User with this email already exists")
        
        hashed_password = self._password_service.hash_password(register_schema.password)

        new_user = User(
            name=register_schema.name,
            email=register_schema.email,
            password=hashed_password
        )

        return self._repository.create(new_user)

    def login(self, login_schema: RequestLoginSchema):
        user = self._repository.get_by_email(login_schema.email)

        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        hashed_stored_password = user.password
        
        if not self._password_service.verify_password(login_schema.password, hashed_stored_password):
            raise HTTPException(status_code=401, detail="Invalid password")

        access_token = self._jwt_service.create_access_token(user.id)
        refresh_token = self._jwt_service.create_refresh_token(user.id)
        
        return ResponseLoginSchema(
            access_token=access_token,
            refresh_token=refresh_token,
            token_type="Bearer"
        )