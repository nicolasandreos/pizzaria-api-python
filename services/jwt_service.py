from datetime import datetime, timedelta, timezone
from jose import jwt
from main import ACCESS_TOKEN_EXPIRE_MINUTES, JWT_TOKEN, ALGORITHM, REFRESH_TOKEN_EXPIRE_MINUTES

class JwtService:

    @staticmethod
    def create_access_token(user_id: int):
        expiration_date = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        payload ={
            "sub": str(user_id),
            "exp": expiration_date
        }
        token = jwt.encode(
            payload,
            JWT_TOKEN,
            algorithm=ALGORITHM
        )
        return token

    @staticmethod
    def create_refresh_token(user_id: int):
        expiration_date = datetime.now(timezone.utc) + timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES)
        payload ={
            "sub": str(user_id),
            "exp": expiration_date
        }
        token = jwt.encode(
            payload,
            JWT_TOKEN,
            algorithm=ALGORITHM
        )
        return token