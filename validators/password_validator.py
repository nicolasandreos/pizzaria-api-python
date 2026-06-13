from exceptions.validation_exception import InvalidTypeException, InvalidPasswordException

class PasswordValidator:

    @staticmethod
    def validate(password: str) -> str:
        if not isinstance(password, str):
            raise InvalidTypeException(expected_type=str, actual_type=type(password), field_name="password")
        if len(password.strip()) < 6:
            raise InvalidPasswordException()
        return password.strip()