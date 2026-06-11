import os

from fastapi import APIRouter, Depends, HTTPException
from models import User
from dependencies import get_session
from main import bcrypt_context, ACCESS_TOKEN_EXPIRE_MINUTES, ALGORITHM, JWT_TOKEN, REFRESH_TOKEN_EXPIRE_MINUTES
from schemas.user_schema import RequestCreateUserSchema, RequestLoginSchema
from sqlalchemy.orm import Session
from jose import jwt
from datetime import datetime, timedelta, timezone

auth_router = APIRouter(prefix="/auth", tags=["auth"])

def create_token(user_id: int, token_duration: timedelta = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)):
    expiration_date = datetime.now(timezone.utc) + token_duration
    payload ={
        "sub": user_id,
        "exp": expiration_date
    }
    token = jwt.encode(
        payload,
        JWT_TOKEN,
        algorithm=ALGORITHM
    )
    return token
    

@auth_router.post("/register")
async def create_account(user_schema: RequestCreateUserSchema, session: Session = Depends(get_session)):
    user_by_email = session.query(User)\
        .filter(User.email == user_schema.email).first()

    if user_by_email:
        raise HTTPException(status_code=409, detail="User with this email already exists")
    
    else:
        hashed_password = bcrypt_context.hash(user_schema.password)
        new_user = User(name=user_schema.name, email=user_schema.email, password=hashed_password)
        session.add(new_user)
        session.commit()
        return {"message": f"User created successfully: Name: {new_user.name} Email: {new_user.email}"}

@auth_router.post("/login")
async def login(login_schema: RequestLoginSchema, session: Session = Depends(get_session)):
    user = session.query(User).filter(User.email == login_schema.email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    if not bcrypt_context.verify(login_schema.password, user.password):
        raise HTTPException(status_code=401, detail="Invalid password")

    access_token = create_token(user.id)
    refresh_token = create_token(user.id, timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES))
    
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "Bearer"
    }