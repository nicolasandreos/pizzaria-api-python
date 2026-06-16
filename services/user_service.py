import logging

from exceptions.user_exceptions import InvalidCurrentPasswordException, InvalidNewPasswordException, UserAlreadyActiveException, UserAlreadyAdminException, UserAlreadyDeactivatedException, UserNotFoundException
from exceptions.validation_exception import InvalidPasswordException
from models.user import User
from repositories.user_repository import UserRepository
from schemas.request.user.change_password_schema import RequestUserChangePasswordSchema
from schemas.request.user.update_user_schema import RequestUpdateUserSchema
from schemas.response.auth.user_schema import ResponseUserSchema
from services.password_service import PasswordService

logger = logging.getLogger(__name__)


class UserService:

    def __init__(self, user_repository: UserRepository):
        self._repository = user_repository


    def get_me(self, user_id: int) -> ResponseUserSchema:
        logger.debug("Fetching profile for authenticated user (user_id=%s)", user_id)
        user = self._repository.get_by_id(user_id)

        return ResponseUserSchema(
            name=user.name,
            email=user.email,
            active=user.active,
            admin=user.admin,
            created_at=user.created_at
        )

    
    def change_password(self, change_password_schema: RequestUserChangePasswordSchema, user: User) -> ResponseUserSchema:
        logger.info("Password change requested (user_id=%s, email=%s)", user.id, user.email)
        is_same_password = PasswordService.verify_password(change_password_schema.current_password, user.password)
        if not is_same_password:
            logger.warning("Password change rejected: current password mismatch (user_id=%s)", user.id)
            raise InvalidCurrentPasswordException()

        is_new_password_same = PasswordService.verify_password(change_password_schema.new_password, user.password)
        if is_new_password_same:
            logger.warning(
                "Password change rejected: new password equals current (user_id=%s)",
                user.id,
            )
            raise InvalidNewPasswordException()

        new_password = PasswordService.hash_password(change_password_schema.new_password)
        user.password = new_password
        self._repository.update(user)
        logger.info("Password changed successfully (user_id=%s, email=%s)", user.id, user.email)

        return ResponseUserSchema(
            name=user.name,
            email=user.email,
            active=user.active,
            admin=user.admin,
            created_at=user.created_at
        )


    def deactivate(self, user_id: int) -> ResponseUserSchema:
        logger.info("User deactivation requested (target_user_id=%s)", user_id)
        user = self._repository.get_by_id(user_id)
        if not user:
            logger.warning("User deactivation failed: user not found (target_user_id=%s)", user_id)
            raise UserNotFoundException()

        if not user.active:
            logger.warning(
                "User deactivation skipped: account already inactive (user_id=%s)",
                user_id,
            )
            raise UserAlreadyDeactivatedException()

        user.active = False
        self._repository.update(user)
        logger.info("User deactivated (user_id=%s, email=%s)", user.id, user.email)

        return ResponseUserSchema(
            name=user.name,
            email=user.email,
            active=user.active,
            admin=user.admin,
            created_at=user.created_at
        )


    def activate(self, user_id: int) -> ResponseUserSchema:
        logger.info("User activation requested (target_user_id=%s)", user_id)
        user = self._repository.get_by_id(user_id)
        if not user:
            logger.warning("User activation failed: user not found (target_user_id=%s)", user_id)
            raise UserNotFoundException()

        if user.active:
            logger.warning(
                "User activation skipped: account already active (user_id=%s)",
                user_id,
            )
            raise UserAlreadyActiveException()

        user.active = True
        self._repository.update(user)
        logger.info("User activated (user_id=%s, email=%s)", user.id, user.email)

        return ResponseUserSchema(
            name=user.name,
            email=user.email,
            active=user.active,
            admin=user.admin,
            created_at=user.created_at
        )


    def activate_admin(self, user_id: int) -> ResponseUserSchema:
        logger.info("Admin grant requested (target_user_id=%s)", user_id)
        user = self._repository.get_by_id(user_id)
        if not user:
            logger.warning("Admin grant failed: user not found (target_user_id=%s)", user_id)
            raise UserNotFoundException()
        
        if user.admin:
            logger.warning("Admin grant skipped: user is already admin (user_id=%s)", user_id)
            raise UserAlreadyAdminException()

        user.admin = True
        self._repository.update(user)
        logger.info("Admin privileges granted (user_id=%s, email=%s)", user.id, user.email)

        return ResponseUserSchema(
            name=user.name,
            email=user.email,
            active=user.active,
            admin=user.admin,
            created_at=user.created_at
        )

    
    def update_profile(self, update_user_schema: RequestUpdateUserSchema, user: User) -> ResponseUserSchema:
        logger.info(
            "Profile update requested (user_id=%s, previous_email=%s, new_email=%s)",
            user.id,
            user.email,
            update_user_schema.email,
        )
        user.name = update_user_schema.name
        user.email = update_user_schema.email
        self._repository.update(user)
        logger.info("Profile updated (user_id=%s, email=%s)", user.id, user.email)

        return ResponseUserSchema(
            name=user.name,
            email=user.email,
            active=user.active,
            admin=user.admin,
            created_at=user.created_at
        )
        