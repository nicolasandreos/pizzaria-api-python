import re
from exceptions.validation_exception import InvalidTypeException, InvalidEmailException

class EmailValidator:

    @staticmethod
    def validate(email: str) -> bool:
        if not isinstance(email, str):
            raise InvalidTypeException(expected_type=str, actual_type=type(email), field_name="email")
        if not re.match(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", email.strip()):
            raise InvalidEmailException()
        return email.strip()