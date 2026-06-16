from repositories.user_repository import UserRepository
from schemas.response.auth.user_schema import ResponseUserSchema


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