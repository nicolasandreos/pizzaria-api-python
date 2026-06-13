from pydantic import BaseModel, field_validator
from validators.email_validator import EmailValidator
from validators.password_validator import PasswordValidator

class RequestLoginSchema(BaseModel):
    email: str
    password: str

    @field_validator("email", mode="before")
    @classmethod
    def validate_email(cls, value) -> str:
        return EmailValidator.validate(value)

    @field_validator("password", mode="before")
    @classmethod
    def validate_password(cls, value) -> str:
        return PasswordValidator.validate(value)