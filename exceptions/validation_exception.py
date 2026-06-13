from .base_exception import BaseException


# TYPE VALIDATION EXCEPTIONS
class InvalidTypeException(BaseException):
    def __init__(self, expected_type: type, actual_type: type, field_name: str):
        super().__init__(
            message=f"Expected type: {expected_type}, actual type: {actual_type} for field: {field_name}",
            status_code=400
        )

# USER VALIDATION EXCEPTIONS
class InvalidEmailException(BaseException):
    def __init__(self):
        super().__init__(
            message="Invalid email address",
            status_code=400
        )

class InvalidPasswordException(BaseException):
    def __init__(self):
        super().__init__(
            message="Password must be at least 6 characters long",
            status_code=400
        )

class InvalidNameException(BaseException):
    def __init__(self):
        super().__init__(
            message="Name must be at least 1 character long",
            status_code=400
        )