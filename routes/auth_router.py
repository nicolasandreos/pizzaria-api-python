from fastapi import APIRouter, Depends
from models import User
from dependencies import get_session
from main import bcrypt_context

auth_router = APIRouter(prefix="/auth", tags=["auth"])

@auth_router.post("/register")
async def create_account(name: str, email: str, password: str, session = Depends(get_session)):
    user_by_email = session.query(User)\
        .filter(User.email == email).first()

    if user_by_email:
        return {"message": "User with this email already exists"}
    
    else:
        hashed_password = bcrypt_context.hash(password)
        new_user = User(name=name, email=email, password=hashed_password)
        session.add(new_user)
        session.commit()
        return {"message": "User created successfully"}