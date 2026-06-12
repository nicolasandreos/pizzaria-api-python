from pydantic import BaseModel, field_validator
import re
from exceptions.validation_exception import InvalidTypeException, InvalidEmailException, InvalidPasswordException

class RequestLoginSchema(BaseModel):
    email: str
    password: str

    @field_validator("email", mode="before")
    @classmethod
    def validate_email(cls, value) -> str:
        if not isinstance(value, str):
            raise InvalidTypeException(expected_type=str, actual_type=type(value), field_name="email")
        if not re.match(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", value.strip()):
            raise InvalidEmailException()
        return value.strip()

    @field_validator("password", mode="before")
    @classmethod
    def validate_password(cls, value) -> str:
        if not isinstance(value, str):
            raise InvalidTypeException(expected_type=str, actual_type=type(value), field_name="password")
        if len(value.strip()) < 6:
            raise InvalidPasswordException()
        return value.strip()