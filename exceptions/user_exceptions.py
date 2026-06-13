from .base_exception import ApplicationException

class UserNotFoundException(ApplicationException):
    def __init__(self):
        super().__init__(
            message="User not found",
            status_code=404
        )
    pass