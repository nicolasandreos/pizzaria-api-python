from pydantic import BaseModel, field_validator
from typing import Optional
from exceptions.validation_exception import InvalidNameException, InvalidTypeException
from validators.email_validator import EmailValidator
from validators.password_validator import PasswordValidator

class RequestCreateUserSchema(BaseModel):
    name: str
    email: str
    password: str
    active: Optional[bool] = None
    admin: Optional[bool] = None

    # permite que o scjhema seja criado a partir dos atributos de um objeto
    class Config:
        from_attributes = True

    @field_validator("name", mode="before")
    @classmethod
    def validate_name(cls, value) -> str:
        if value.strip() == "":
            raise InvalidNameException()
        if not isinstance(value, str):
            raise InvalidTypeException(expected_type=str, actual_type=type(value), field_name="name")
        return value.strip()

    @field_validator("email", mode="before")
    @classmethod
    def validate_email(cls, value) -> str:
        return EmailValidator.validate(value)

    @field_validator("password", mode="before")
    @classmethod
    def validate_password(cls, value) -> str:
        return PasswordValidator.validate(value)

    @field_validator("active", mode="before")
    @classmethod
    def validate_active(cls, value) -> bool:
        if value is not None and not isinstance(value, bool):
            raise InvalidTypeException(expected_type=bool, actual_type=type(value), field_name="active")
        return value
    
    @field_validator("admin", mode="before")
    @classmethod
    def validate_admin(cls, value) -> bool:
        if value is not None and not isinstance(value, bool):
            raise InvalidTypeException(expected_type=bool, actual_type=type(value), field_name="admin")
        return value
        