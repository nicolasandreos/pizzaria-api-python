from services.jwt_service import JwtService
from fastapi import Depends

def get_jwt_service():
    return JwtService()