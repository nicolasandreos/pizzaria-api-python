from models import db, User
from sqlalchemy.orm import sessionmaker, Session
from fastapi import Depends, HTTPException
from jose import jwt, JWTError
from main import JWT_TOKEN, ALGORITHM, oauth2_schema
from datetime import datetime, timezone

def get_session():
    try:
        Session = sessionmaker(bind=db)
        session = Session()
        yield session
    except Exception as e:
        print(e)
        raise
    finally:
        session.close()


def verify_token(token: str = Depends(oauth2_schema), session: Session = Depends(get_session)):

    try:
        payload =jwt.decode(token, JWT_TOKEN, algorithms=[ALGORITHM])
        user_id = int(payload.get("sub"))
        expiration_date = payload.get("exp")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

    user = session.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    if is_token_expired(expiration_date):
        raise HTTPException(status_code=401, detail="Token expired")
    return user

def is_token_expired(expiration_date: datetime):
    datetime_expiration = datetime.fromtimestamp(expiration_date, timezone.utc)
    return datetime.now(timezone.utc) > datetime_expiration