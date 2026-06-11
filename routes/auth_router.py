import os

from fastapi import APIRouter, Depends, HTTPException
from models import User
from dependencies import get_session
from main import bcrypt_context
from schemas.user_schema import RequestCreateUserSchema, RequestLoginSchema
from sqlalchemy.orm import Session
from jose import jwt

auth_router = APIRouter(prefix="/auth", tags=["auth"])

def create_token(user_id: int):
    access_token = jwt.encode(
        {"sub": user_id},
        os.getenv("JWT_TOKEN"),
        algorithm="HS256"
    )
    return access_token
    

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
    
    return {
        "access_token": access_token,
        "token_type": "Bearer"
    }