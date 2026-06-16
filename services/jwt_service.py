import logging
from datetime import datetime, timedelta, timezone
from jose import jwt
from main import ACCESS_TOKEN_EXPIRE_MINUTES, JWT_TOKEN, ALGORITHM, REFRESH_TOKEN_EXPIRE_MINUTES

logger = logging.getLogger(__name__)


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
        logger.debug(
            "Access token issued (user_id=%s, expires_at=%s)",
            user_id,
            expiration_date.isoformat(),
        )

        return access_token

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
        logger.debug(
            "Refresh token issued (user_id=%s, expires_at=%s)",
            user_id,
            expiration_date.isoformat(),
        )
        return refresh_token

    @staticmethod
    def generate_tokens(user_id: int) -> tuple[str, str]:
        logger.info("Generating auth token pair (user_id=%s)", user_id)
        access_token = JwtService.create_access_token(user_id)
        refresh_token = JwtService.create_refresh_token(user_id)
        return access_token, refresh_token