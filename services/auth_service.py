import logging

from repositories.user_repository import UserRepository
from schemas.request.auth.create_user_schema import RequestCreateUserSchema
from schemas.request.auth.login_user_schema import RequestLoginSchema
from schemas.response.auth.login_schema import ResponseLoginSchema
from schemas.response.auth.create_user_schema import ResponseCreateUserSchema
from services.password_service import PasswordService
from models import User
from services.jwt_service import JwtService
from fastapi.security import OAuth2PasswordRequestForm
from exceptions.user_exceptions import UserNotFoundException
from exceptions.auth_exceptions import InvalidCredentialsException, UserAlreadyExistsException

logger = logging.getLogger(__name__)


class AuthService:

    def __init__(self, user_repository: UserRepository, password_service: PasswordService):
        self._repository = user_repository
        self._password_service = password_service

    def register(self, register_schema: RequestCreateUserSchema, is_admin: bool = False) -> ResponseCreateUserSchema:
        logger.info(
            "User registration requested (email=%s, admin=%s)",
            register_schema.email,
            is_admin,
        )
        user = self._repository.get_by_email(register_schema.email)

        if user:
            logger.warning(
                "Registration rejected: email already registered (email=%s)",
                register_schema.email,
            )
            raise UserAlreadyExistsException()
        
        hashed_password = self._password_service.hash_password(register_schema.password)

        new_user = User(
            name=register_schema.name,
            email=register_schema.email,
            password=hashed_password,
            admin=is_admin
        )

        created_user = self._repository.create(new_user)
        logger.info(
            "User registered successfully (user_id=%s, email=%s, admin=%s)",
            created_user.id,
            created_user.email,
            created_user.admin,
        )

        return ResponseCreateUserSchema(
            name=created_user.name,
            email=created_user.email,
            active=created_user.active,
            admin=created_user.admin
        )

    def login(self, login_schema: RequestLoginSchema) -> ResponseLoginSchema:
        logger.info("Login attempt (email=%s)", login_schema.email)
        user = self._authenticate_user(login_schema.email, login_schema.password)
        access_token, refresh_token = JwtService.generate_tokens(user.id)
        logger.info("Login successful (user_id=%s, email=%s)", user.id, user.email)

        return ResponseLoginSchema(
            access_token=access_token,
            refresh_token=refresh_token,
            token_type="Bearer"
        )

    def login_form_docs(self, form_data: OAuth2PasswordRequestForm) -> ResponseLoginSchema:
        logger.info("OAuth2 form login attempt (username=%s)", form_data.username)
        user = self._authenticate_user(form_data.username, form_data.password)
        access_token, refresh_token = JwtService.generate_tokens(user.id)
        logger.info("OAuth2 form login successful (user_id=%s, email=%s)", user.id, user.email)

        return ResponseLoginSchema(
            access_token=access_token,
            refresh_token=refresh_token,
            token_type="Bearer"
        )

    def _authenticate_user(self, email: str, password: str) -> User:
        user = self._repository.get_by_email(email)
        if not user:
            logger.warning("Authentication failed: user not found (email=%s)", email)
            raise UserNotFoundException()
        
        hashed_stored_password = user.password
        if not self._password_service.verify_password(password, hashed_stored_password):
            logger.warning(
                "Authentication failed: invalid credentials (user_id=%s, email=%s)",
                user.id,
                email,
            )
            raise InvalidCredentialsException()
        return user
