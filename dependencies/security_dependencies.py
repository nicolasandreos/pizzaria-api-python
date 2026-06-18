from dependencies.session_dependencies import get_session
from models import User
from sqlalchemy.orm import Session
from fastapi import Depends
from jose import jwt, JWTError
from settings import settings
from main import oauth2_schema
from datetime import datetime, timezone
from exceptions.auth_exceptions import InvalidRefreshTokenException
from exceptions.user_exceptions import UserNotFoundException
from exceptions.auth_exceptions import TokenNotFoundException

def verify_token(token: str | None = Depends(oauth2_schema), session: Session = Depends(get_session)) -> User | None:

    if not token:
        raise TokenNotFoundException()

    try:
        payload =jwt.decode(token, settings.JWT_TOKEN, algorithms=[settings.ALGORITHM])
        user_id = int(payload.get("sub"))
        expiration_date = payload.get("exp")
    except JWTError:
        raise InvalidRefreshTokenException()

    user = session.query(User).filter(User.id == user_id).first()
    if not user:
        raise UserNotFoundException()
    if _is_token_expired(expiration_date):
        raise InvalidRefreshTokenException()
    return user


def _is_token_expired(expiration_date: datetime):
    datetime_expiration = datetime.fromtimestamp(expiration_date, timezone.utc)
    return datetime.now(timezone.utc) > datetime_expiration