from fastapi import Depends
from dependencies.security_dependencies import verify_token
from models import User
from exceptions.auth_exceptions import UserIsNotAdminException

def get_admin_user(user: User = Depends(verify_token)):
    if not user.admin:
        raise UserIsNotAdminException()
    return user