from passlib.context import CryptContext

_bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class PasswordService:

    @staticmethod
    def hash_password(password: str) -> str:
        return _bcrypt_context.hash(password)

    @staticmethod
    def verify_password(password: str, hashed_password: str) -> bool:
        return _bcrypt_context.verify(password, hashed_password)
