from tests.conftest import client
from services.jwt_service import JwtService

def test_login_should_return_401_when_invalid_credentials():
    response = client.post("/auth/login", json={"email": "test@example.com", "password": "12345678"})

    assert response.status_code == 401

def test_login_should_return_200_when_valid_credentials():
    response = client.post("/auth/login", json={"email": "test@example.com", "password": "123456"})

    assert response.status_code == 200


def test_login_should_return_401_when_inactive_user():
    response = client.post("/auth/login", json={"email": "inactive@example.com", "password": "123456"})

    assert response.status_code == 401


def test_login_should_return_404_when_user_not_found():
    response = client.post("/auth/login", json={"email": "notfound@example.com", "password": "123456"})

    assert response.status_code == 404


def test_register_should_return_201_when_valid_user():
    response = client.post("/auth/register", json={"email": "test2@example.com", "password": "123456", "name": "test2"})

    assert response.status_code == 201


def test_register_should_return_409_when_user_already_exists():
    response = client.post("/auth/register", json={"email": "test@example.com", "password": "123456", "name": "test"})

    assert response.status_code == 409

def test_refresh_access_token_should_return_200_when_valid_token():
    user_id = 1
    refresh_token = JwtService.create_refresh_token(user_id)
    response = client.post("/auth/refresh-access-token", headers={"Authorization": f"Bearer {refresh_token}"})

    assert response.status_code == 200

def test_refresh_access_token_should_return_401_when_invalid_token():
    response = client.post("/auth/refresh-access-token", headers={"Authorization": "Bearer invalid"})

    assert response.status_code == 401

def refresh_access_token_should_return_access_token():
    user_id = 1
    refresh_token = JwtService.create_refresh_token(user_id)
    response = client.post("/auth/refresh-access-token", headers={"Authorization": f"Bearer {refresh_token}"})

    assert response.json()["access_token"] is not None
    assert response.json()["token_type"] == "Bearer"