from jose import jwt
from main import JWT_TOKEN, ALGORITHM
from services.jwt_service import JwtService
from datetime import datetime, timezone

def test_generate_access_token():
    test_user_id = 1
    result = JwtService.create_access_token(test_user_id)
    assert result is not None
    assert isinstance(result, str)
    assert len(result) > 0

def test_generate_refresh_token():
    test_user_id = 1
    result = JwtService.create_refresh_token(test_user_id)
    assert result is not None
    assert isinstance(result, str)
    assert len(result) > 0

def test_access_token_should_store_valid_payload():
    test_user_id = 1
    access_token = JwtService.create_access_token(test_user_id)
    payload = jwt.decode(access_token, JWT_TOKEN, algorithms=[ALGORITHM])
    assert payload is not None
    assert payload.get("sub") == str(test_user_id)
    assert payload.get("exp") is not None


def test_refresh_token_should_store_valid_payload():
    test_user_id = 1
    refresh_token = JwtService.create_refresh_token(test_user_id)
    payload = jwt.decode(refresh_token, JWT_TOKEN, algorithms=[ALGORITHM])
    assert payload is not None
    assert payload.get("sub") == str(test_user_id)
    assert payload.get("exp") is not None


def test_access_token_expiration_date():
    test_user_id = 1
    access_token = JwtService.create_access_token(test_user_id)
    payload = jwt.decode(access_token, JWT_TOKEN, algorithms=[ALGORITHM])
    expiration_date = datetime.fromtimestamp(payload.get("exp"), timezone.utc)
    now = datetime.now(timezone.utc)

    minutes = (
        expiration_date - now
    ).total_seconds() / 60
    assert 28 <= minutes <= 30

def test_refresh_token_expiration_date():
    test_user_id = 1
    refresh_token = JwtService.create_refresh_token(test_user_id)
    payload = jwt.decode(refresh_token, JWT_TOKEN, algorithms=[ALGORITHM])
    expiration_date = datetime.fromtimestamp(payload.get("exp"), timezone.utc)
    now = datetime.now(timezone.utc)

    days = (
        expiration_date - now
    ).total_seconds() / 86400
    assert 6 <= days <= 7