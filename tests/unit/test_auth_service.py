import pytest

from unittest.mock import Mock
from exceptions.auth_exceptions import InvalidCredentialsException, UserAlreadyExistsException
from exceptions.user_exceptions import UserNotFoundException
from models.user import User
from schemas.request.auth.create_user_schema import RequestCreateUserSchema
from schemas.request.auth.login_user_schema import RequestLoginSchema
from services.auth_service import AuthService

def test_login_should_return_valid_token():
    repository_mock = Mock()
    password_service_mock = Mock()
    jwt_service_mock = Mock()

    auth_service = AuthService(repository_mock, password_service_mock, jwt_service_mock)

    user = User(name="test", email="test@example.com", password="12345678")
    user.id = 1
    repository_mock.get_by_email.return_value = user
    password_service_mock.verify_password.return_value = True
    jwt_service_mock.generate_tokens.return_value = ("access_token", "refresh_token")

    result = auth_service.login(RequestLoginSchema(email="test@example.com", password="12345678"))

    assert result.access_token == "access_token"
    assert result.refresh_token == "refresh_token"
    assert result.token_type == "Bearer"


def test_login_should_raise_user_not_found_exception():
    repository_mock = Mock()
    password_service_mock = Mock()
    jwt_service_mock = Mock()

    auth_service = AuthService(repository_mock, password_service_mock, jwt_service_mock)

    repository_mock.get_by_email.return_value = None
    with pytest.raises(UserNotFoundException):
        auth_service.login(RequestLoginSchema(email="test@example.com", password="12345678"))


def test_login_should_raise_invalid_credentials_exception():
    repository_mock = Mock()
    password_service_mock = Mock()
    jwt_service_mock = Mock()
    user = User(name="test", email="test@example.com", password="12345678")
    user.id = 1

    repository_mock.get_by_email.return_value = user
    password_service_mock.verify_password.return_value = False

    auth_service = AuthService(repository_mock, password_service_mock, jwt_service_mock)

    with pytest.raises(InvalidCredentialsException):
        auth_service.login(RequestLoginSchema(email="test@example.com", password="12345678"))


def test_register_should_return_valid_user_saved_in_database():
    repository_mock = Mock()
    password_service_mock = Mock()
    jwt_service_mock = Mock()

    auth_service = AuthService(repository_mock, password_service_mock, jwt_service_mock)

    user = User(name="test", email="test@example.com", password="12345678")
    user.id = 1

    repository_mock.get_by_email.return_value = None
    password_service_mock.hash_password.return_value = "hashed_password"
    repository_mock.create.return_value = user

    result = auth_service.register(RequestCreateUserSchema(name="test", email="test@example.com", password="12345678"))

    assert result.name == "test"
    assert result.email == "test@example.com"
    assert result.active == True
    assert result.admin == False


def test_register_should_raise_user_already_exists_exception():
    repository_mock = Mock()
    password_service_mock = Mock()
    jwt_service_mock = Mock()

    auth_service = AuthService(repository_mock, password_service_mock, jwt_service_mock)

    user = User(name="test", email="test@example.com", password="12345678")
    user.id = 1

    repository_mock.get_by_email.return_value = user
    with pytest.raises(UserAlreadyExistsException):
        auth_service.register(RequestCreateUserSchema(name="test", email="test@example.com", password="12345678"))