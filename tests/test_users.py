from app import schemas
from jose import jwt
from .database import client, session
import pytest
from app.config import settings




def test_create_user(client):
    res = client.post("/users/", json={"email": "test@example.com", "password": "password123"})
    new_user = schemas.UserOut(**res.json())
    assert new_user.email == "test@example.com"
    assert res.status_code == 201
    
#def test_root(client):
#    res = client.get("/")
#    print(res.json())
#    assert res.json().get("message") == "Bind mount is now working"
#    assert res.status_code == 200



def test_login_user(client, test_user):
    res = client.post("/login", data={"username": test_user['email'], "password": test_user['password']})
    login_res = schemas.Token(**res.json())
    payload = jwt.decode(login_res.access_token, settings.secret_key, algorithms=[settings.algorithm])
    id = payload.get("user_id")
    assert id == str(test_user['id'])
    assert login_res.token_type == "bearer"
    assert res.status_code == 200