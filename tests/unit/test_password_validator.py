import pytest
from validators.password_validator import PasswordValidator
from exceptions.validation_exception import InvalidPasswordException, InvalidTypeException

def test_should_accept_valid_password():
    test_password = "12345678"
    result = PasswordValidator.validate(test_password)
    assert result == test_password

def test_should_reject_invalid_password():
    invalid_password = "1234"
    with pytest.raises(InvalidPasswordException):
        PasswordValidator.validate(invalid_password)

def test_should_reject_invalid_type():
    invalid_type = 123
    with pytest.raises(InvalidTypeException):
        PasswordValidator.validate(invalid_type)

def test_should_remove_whitespace_from_password():
    test_password = " 12345678 "
    result = PasswordValidator.validate(test_password)
    assert result == "12345678"