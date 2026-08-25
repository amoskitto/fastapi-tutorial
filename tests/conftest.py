from fastapi import FastAPI
from fastapi.testclient import TestClient
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from app.main import app

from app.config import settings
from app.database import get_db
from app.database import Base
from app.oauth2 import create_access_token
from app import models

DATABASE_URL = f'postgresql+psycopg://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}'

engine = create_engine(DATABASE_URL)

TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        
app.dependency_overrides[get_db] = override_get_db

@pytest.fixture()
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture()
def client(session):
    def override_get_db():
        try:
            yield session
        finally:
            session.close()
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    
@pytest.fixture
def test_user(client):
    user_data = {"email":  "test@example.com",
                "password": "password123"}
    res = client.post("/users/", json=user_data)
    assert res.status_code == 201
    new_user = res.json()
    new_user['password'] = user_data['password']
    return new_user



@pytest.fixture
def token(test_user):
    return create_access_token({"user_id": test_user['id']})


@pytest.fixture
def authorized_client(client, token):
    client.headers = {
        **client.headers,
        "Authorization": f"Bearer {token}"
    }
    return client

@pytest.fixture
def test_posts(test_user, session):
    posts_data = [
        {"title": "First Post", "content": "Content of the first post", "owner_id": test_user['id']},
        {"title": "Second Post", "content": "Content of the second post", "owner_id": test_user['id']},
        {"title": "Third Post", "content": "Content of the third post", "owner_id": test_user['id']}
    ]
    
    def create_post_model(post):
        return models.Post(**post)
    
        # 1. Convert raw data to model objects
    posts_to_add = list(map(create_post_model, posts_data))

    # 2. Add them to database session
    session.add_all(posts_to_add)
    session.commit()

    # 3. Fetch all posts (including the new ones)
    posts = session.query(models.Post).all()  # Now includes newly added ones
    return posts