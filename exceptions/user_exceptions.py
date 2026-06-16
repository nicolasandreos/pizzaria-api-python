from .base_exception import ApplicationException

class UserNotFoundException(ApplicationException):
    def __init__(self):
        super().__init__(
            message="User not found",
            status_code=404
        )
    pass

class ProductNotFoundException(ApplicationException):
    def __init__(self):
        super().__init__(
            message="Product not found",
            status_code=404
        )
    pass

class InvalidCurrentPasswordException(ApplicationException):
    def __init__(self):
        super().__init__(
            message="Current password is not correct",
            status_code=400
        )
    pass

class InvalidNewPasswordException(ApplicationException):
    def __init__(self):
        super().__init__(
            message="New password is the same as the current password",
            status_code=400
        )
    pass

class UserAlreadyDeactivatedException(ApplicationException):
    def __init__(self):
        super().__init__(
            message="User is already deactivated",
            status_code=400
        )
    pass

class UserAlreadyActiveException(ApplicationException):
    def __init__(self):
        super().__init__(
            message="User is already active",
            status_code=400
        )
    pass
