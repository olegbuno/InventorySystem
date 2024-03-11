import pytest
from fastapi.testclient import TestClient
from passlib.context import CryptContext
from sqlalchemy.orm import sessionmaker

from app.database import engine, get_user_by_username, create_user
from main import app

# Create a testing session for the database
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Instantiate the test client
client = TestClient(app)

# Fixture to obtain an authentication token
@pytest.fixture(scope="module")
def auth_token():
    # Check if the user exists, create if not
    with TestingSessionLocal() as db:
        user = get_user_by_username("test_user", db)
        if not user:
            # Password hashing
            pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
            hashed_password = pwd_context.hash('test_password')
            create_user(username="test_user", password_hash=hashed_password, db=db)

    login_data = {
        "username": "test_user",
        "password": "test_password"
    }
    response = client.post("/login/", data=login_data)
    return response.json()["access_token"]


def make_authenticated_request(method, url, token=None, **kwargs):
    headers = {}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    return client.request(method, url, headers=headers, **kwargs)


def test_create_item(auth_token):
    item_data = {
        "name": "Test Item",
        "description": "Test Description",
        "category": "Test Category",
        "quantity": 10,
        "price": 50.0
    }
    response = make_authenticated_request("POST", "/items/", token=auth_token, json=item_data)

    assert response.status_code == 200
    item = response.json()
    assert item["name"] == "Test Item"
    assert item["description"] == "Test Description"
    assert item["category"] == "Test Category"
    assert item["quantity"] == 10
    assert item["price"] == 50.0


def test_read_items(auth_token):
    response = make_authenticated_request("GET", "/items/", token=auth_token)

    assert response.status_code == 200
    items = response.json()
    assert len(items) > 0


def test_read_item(auth_token):
    response = make_authenticated_request("GET", "/items/1", token=auth_token)

    assert response.status_code == 200
    item = response.json()
    assert item["id"] == 1


def test_update_item(auth_token):
    item_data = {
        "name": "Updated Item Name",
        "description": "Updated Description",
        "category": "Updated Category",
        "quantity": 20,
        "price": 100.0
    }
    response = make_authenticated_request("PUT", "/items/1", token=auth_token, json=item_data)

    assert response.status_code == 200
    item = response.json()
    assert item["name"] == "Updated Item Name"
    assert item["description"] == "Updated Description"
    assert item["category"] == "Updated Category"
    assert item["quantity"] == 20
    assert item["price"] == 100.0


def test_delete_item(auth_token):
    response = make_authenticated_request("DELETE", "/items/1", token=auth_token)

    assert response.status_code == 200
    item = response.json()
    assert item["id"] == 1
