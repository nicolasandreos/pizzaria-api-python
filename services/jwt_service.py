from datetime import datetime, timedelta, timezone
from jose import jwt
from main import ACCESS_TOKEN_EXPIRE_MINUTES, JWT_TOKEN, ALGORITHM, REFRESH_TOKEN_EXPIRE_MINUTES
from schemas.response.auth.access_token_schema import ResponseAccessTokenSchema
from schemas.response.auth.refresh_token_schema import ResponseRefreshTokenSchema

class JwtService:

    @staticmethod
    def create_access_token(user_id: int):
        expiration_date = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        payload ={
            "sub": str(user_id),
            "exp": expiration_date
        }
        access_token = jwt.encode(
            payload,
            JWT_TOKEN,
            algorithm=ALGORITHM
        )

        return ResponseAccessTokenSchema(
            access_token=access_token,
            token_type="Bearer"
        )

    @staticmethod
    def create_refresh_token(user_id: int):
        expiration_date = datetime.now(timezone.utc) + timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES)
        payload ={
            "sub": str(user_id),
            "exp": expiration_date
        }
        refresh_token = jwt.encode(
            payload,
            JWT_TOKEN,
            algorithm=ALGORITHM
        )
        return ResponseRefreshTokenSchema(
            refresh_token=refresh_token,
            token_type="Bearer"
        )