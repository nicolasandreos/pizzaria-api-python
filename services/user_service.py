from exceptions.user_exceptions import InvalidCurrentPasswordException, InvalidNewPasswordException, UserAlreadyActiveException, UserAlreadyAdminException, UserAlreadyDeactivatedException, UserNotFoundException
from exceptions.validation_exception import InvalidPasswordException
from models.user import User
from repositories.user_repository import UserRepository
from schemas.request.user.change_password_schema import RequestUserChangePasswordSchema
from schemas.request.user.update_user_schema import RequestUpdateUserSchema
from schemas.response.auth.user_schema import ResponseUserSchema
from services.password_service import PasswordService


class UserService:

    def __init__(self, user_repository: UserRepository):
        self._repository = user_repository


    def get_me(self, user_id: int) -> ResponseUserSchema:
        user = self._repository.get_by_id(user_id)

        return ResponseUserSchema(
            name=user.name,
            email=user.email,
            active=user.active,
            admin=user.admin,
            created_at=user.created_at
        )

    
    def change_password(self, change_password_schema: RequestUserChangePasswordSchema, user: User) -> ResponseUserSchema:
        is_same_password = PasswordService.verify_password(change_password_schema.current_password, user.password)
        if not is_same_password:
            raise InvalidCurrentPasswordException()

        is_new_password_same = PasswordService.verify_password(change_password_schema.new_password, user.password)
        if is_new_password_same:
            raise InvalidNewPasswordException()

        new_password = PasswordService.hash_password(change_password_schema.new_password)
        user.password = new_password
        self._repository.update(user)

        return ResponseUserSchema(
            name=user.name,
            email=user.email,
            active=user.active,
            admin=user.admin,
            created_at=user.created_at
        )


    def deactivate(self, user_id: int) -> ResponseUserSchema:
        user = self._repository.get_by_id(user_id)
        if not user:
            raise UserNotFoundException()

        if not user.active:
            raise UserAlreadyDeactivatedException()

        user.active = False
        self._repository.update(user)

        return ResponseUserSchema(
            name=user.name,
            email=user.email,
            active=user.active,
            admin=user.admin,
            created_at=user.created_at
        )


    def activate(self, user_id: int) -> ResponseUserSchema:
        user = self._repository.get_by_id(user_id)
        if not user:
            raise UserNotFoundException()

        if user.active:
            raise UserAlreadyActiveException()

        user.active = True
        self._repository.update(user)

        return ResponseUserSchema(
            name=user.name,
            email=user.email,
            active=user.active,
            admin=user.admin,
            created_at=user.created_at
        )


    def activate_admin(self, user_id: int) -> ResponseUserSchema:
        user = self._repository.get_by_id(user_id)
        if not user:
            raise UserNotFoundException()
        
        if user.admin:
            raise UserAlreadyAdminException()

        user.admin = True
        self._repository.update(user)

        return ResponseUserSchema(
            name=user.name,
            email=user.email,
            active=user.active,
            admin=user.admin,
            created_at=user.created_at
        )

    
    def update_profile(self, update_user_schema: RequestUpdateUserSchema, user: User) -> ResponseUserSchema:
        user.name = update_user_schema.name
        user.email = update_user_schema.email
        self._repository.update(user)

        return ResponseUserSchema(
            name=user.name,
            email=user.email,
            active=user.active,
            admin=user.admin,
            created_at=user.created_at
        )
        