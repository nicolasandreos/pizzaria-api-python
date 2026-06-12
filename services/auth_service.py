from repositories.user_repository import UserRepository
from schemas.request.auth.create_user_schema import RequestCreateUserSchema
from schemas.request.auth.login_user_schema import RequestLoginSchema
from schemas.response.auth.login_schema import ResponseLoginSchema
from schemas.response.auth.create_user_schema import ResponseCreateUserSchema
from fastapi import HTTPException
from services.password_service import PasswordService
from models import User
from services.jwt_service import JwtService
from fastapi.security import OAuth2PasswordRequestForm
class AuthService:

    def __init__(self, user_repository: UserRepository, password_service: PasswordService, jwt_service: JwtService):
        self._repository = user_repository
        self._password_service = password_service
        self._jwt_service = jwt_service

    def register(self, register_schema: RequestCreateUserSchema) -> ResponseCreateUserSchema:
        user = self._repository.get_by_email(register_schema.email)

        if user:
            raise HTTPException(status_code=409, detail="User with this email already exists")
        
        hashed_password = self._password_service.hash_password(register_schema.password)

        new_user = User(
            name=register_schema.name,
            email=register_schema.email,
            password=hashed_password
        )

        created_user = self._repository.create(new_user)

        return ResponseCreateUserSchema(
            name=created_user.name,
            email=created_user.email,
            active=created_user.active,
            admin=created_user.admin
        )

    def login(self, login_schema: RequestLoginSchema) -> ResponseLoginSchema:
        user = self._authenticate_user(login_schema.email, login_schema.password)
        access_token, refresh_token = self._generate_tokens(user)
        
        return ResponseLoginSchema(
            access_token=access_token,
            refresh_token=refresh_token,
            token_type="Bearer"
        )

    def login_form_docs(self, form_data: OAuth2PasswordRequestForm) -> ResponseLoginSchema:
        user = self._authenticate_user(form_data.username, form_data.password)
        access_token, refresh_token = self._generate_tokens(user)

        return ResponseLoginSchema(
            access_token=access_token,
            refresh_token=refresh_token,
            token_type="Bearer"
        )

    def _authenticate_user(self, email: str, password: str) -> User:
        user = self._repository.get_by_email(email)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        hashed_stored_password = user.password
        if not self._password_service.verify_password(password, hashed_stored_password):
            raise HTTPException(status_code=401, detail="Invalid password")
        return user


    def _generate_tokens(self, user: User) -> tuple[str, str]:
        access_token = self._jwt_service.create_access_token(user.id)
        refresh_token = self._jwt_service.create_refresh_token(user.id)
        return access_token, refresh_token