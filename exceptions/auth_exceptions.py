from .base_exception import BaseException

class InvalidCredentialsException(BaseException):
    def __init__(self):
        super().__init__(
            message="Invalid credentials",
            status_code=401
        )


class UserAlreadyExistsException(BaseException):
    def __init__(self):
        super().__init__(
            message="User already exists",
            status_code=409
        )


class InvalidRefreshTokenException(BaseException):
    def __init__(self):
        super().__init__(
            message="Invalid refresh token",
            status_code=401
        )
