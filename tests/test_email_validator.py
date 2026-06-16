import pytest

from exceptions.validation_exception import InvalidEmailException, InvalidTypeException
from validators.email_validator import EmailValidator

def test_should_accept_valid_email():
    test_email = "test@example.com"
    result = EmailValidator.validate(test_email)
    assert result == test_email


def test_should_reject_invalid_email():
    invalid_email = "invalid_email"
    with pytest.raises(InvalidEmailException):
        EmailValidator.validate(invalid_email)

def test_should_reject_invalid_type():
    invalid_type = 123
    with pytest.raises(InvalidTypeException):
        EmailValidator.validate(invalid_type)

def test_should_remove_whitespace_from_email():
    test_email = " test@example.com "
    result = EmailValidator.validate(test_email)
    assert result == "test@example.com"