from passlib.context import CryptContext

class PasswordService:

    def __init__(self):
        self.bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def hash_password(self, password: str):
        return self.bcrypt_context.hash(password)

    def verify_password(self, password: str, hashed_password: str):
        return self.bcrypt_context.verify(password, hashed_password)