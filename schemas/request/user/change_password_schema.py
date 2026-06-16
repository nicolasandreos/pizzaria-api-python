from pydantic import BaseModel, field_validator
from validators.password_validator import PasswordValidator

class RequestUserChangePasswordSchema(BaseModel):
    current_password: str
    new_password: str

    @field_validator("current_password", mode="before")
    @classmethod
    def validate_current_password(cls, value) -> str:
        return PasswordValidator.validate(value)

    @field_validator("new_password", mode="before")
    @classmethod
    def validate_new_password(cls, value) -> str:
        return PasswordValidator.validate(value)
