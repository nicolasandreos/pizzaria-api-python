from pydantic import BaseModel, field_validator, Field

from validators.email_validator import EmailValidator


class RequestUpdateUserSchema(BaseModel):
    name: str = Field(min_length=2, max_length=255)
    email: str

    @field_validator("email", mode="before")
    @classmethod
    def validate_email(cls, value) -> str:
        return EmailValidator.validate(value)