from app import schemas
from .database import client, session
import pytest


@pytest.fixture
def test_user(client):
    user_data = {"email":  "test@example.com",
                "password": "password123"}
    res = client.post("/users/", json=user_data)
    assert res.status_code == 201
    new_user = res.json()
    new_user['password'] = user_data['password']
    return new_user
    
#def test_root(client):
#    res = client.get("/")
#    print(res.json())
#    assert res.json().get("message") == "Bind mount is now working"
#    assert res.status_code == 200

def test_create_user(client):
    res = client.post("/users/", json={"email": "test@example.com", "password": "password123"})
    new_user = schemas.UserOut(**res.json())
    assert new_user.email == "test@example.com"
    assert res.status_code == 201

def test_login_user(client, test_user):
    res = client.post("/login", data={"username": test_user['email'], "password": test_user['password']})
    assert res.status_code == 200