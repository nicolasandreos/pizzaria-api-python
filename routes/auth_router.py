from fastapi import APIRouter, Depends, HTTPException
from models import User
from dependencies import get_session
from main import bcrypt_context
from schemas.user_schema import UserSchema
from sqlalchemy.orm import Session

auth_router = APIRouter(prefix="/auth", tags=["auth"])

@auth_router.post("/register")
async def create_account(user_schema: UserSchema, session: Session = Depends(get_session)):
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