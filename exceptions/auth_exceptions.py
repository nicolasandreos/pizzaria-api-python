from .base_exception import ApplicationException

class InvalidCredentialsException(ApplicationException):
    def __init__(self):
        super().__init__(
            message="Invalid credentials",
            status_code=401
        )


class UserAlreadyExistsException(ApplicationException):
    def __init__(self):
        super().__init__(
            message="User already exists",
            status_code=409
        )


class InvalidRefreshTokenException(ApplicationException):
    def __init__(self):
        super().__init__(
            message="Invalid refresh token",
            status_code=401
        )

class UserNotActiveException(ApplicationException):
    def __init__(self):
        super().__init__(
            message="User is not active and is forbidden to create an order",
            status_code=403
        )

class UserIsNotAdminException(ApplicationException):
    def __init__(self):
        super().__init__(
            message="User is not admin and is forbidden to get all orders",
            status_code=403
        )