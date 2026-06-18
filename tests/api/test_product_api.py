from services.jwt_service import JwtService
from tests.conftest import client

def test_create_product_should_return_403_when_unauthorized():
    user_id = 1 # normal user
    headers = {"Authorization": f"Bearer {JwtService.create_access_token(user_id)}"}
    response = client.post("/products/create", 
        json={"name": "Product 1", "price": 100, "size": "small", "description": "Product 1 description"}, 
        headers=headers)

    assert response.status_code == 403

def test_create_product_should_return_201_when_authorized():
    user_id = 2 # admin user
    headers = {"Authorization": f"Bearer {JwtService.create_access_token(user_id)}"}
    response = client.post("/products/create", 
        json={"name": "Product 1", "price": 100, "size": "SMALL", "description": "Product 1 description"}, 
        headers=headers)

    assert response.status_code == 201


def test_create_product_should_return_422_when_invalid_data():
    user_id = 2 # admin user
    headers = {"Authorization": f"Bearer {JwtService.create_access_token(user_id)}"}
    response = client.post("/products/create", 
        json={"name": "Product 1", "price": -100, "size": "small", "description": "Product 1 description"}, 
        headers=headers)

    assert response.status_code == 422


def test_update_product_should_return_403_when_unauthorized():
    user_id = 1 # normal user
    headers = {"Authorization": f"Bearer {JwtService.create_access_token(user_id)}"}
    response = client.put("/products/update/1", 
        json={"name": "Product 1", "price": 100, "size": "SMALL", "description": "Product 1 description"}, 
        headers=headers)

    assert response.status_code == 403

def test_update_product_should_return_200_when_authorized():
    user_id = 2 # admin user
    headers = {"Authorization": f"Bearer {JwtService.create_access_token(user_id)}"}
    response = client.put("/products/update/1", 
        json={"name": "Product 1", "price": 100, "size": "SMALL", "description": "Product 1 description"}, 
        headers=headers)

    assert response.status_code == 200