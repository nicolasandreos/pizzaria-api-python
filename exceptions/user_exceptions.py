from base_exception import BaseException

class UserNotFoundException(BaseException):
    def __init__(self):
        super().__init__(
            message="User not found",
            status_code=404
        )
    pass