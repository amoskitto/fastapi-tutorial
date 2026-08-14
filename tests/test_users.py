from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from app.main import app
from app import schemas
from app.config import settings
from app.database import get_db
from app.database import Base

DATABASE_URL = f'postgresql+psycopg://{settings.database_username}:{settings.database_password}@{settings.database_hostname}/fastapi_test'

engine = create_engine(DATABASE_URL)

TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base.metadata.create_all(bind=engine)



def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        
app.dependency_overrides[get_db] = override_get_db


client = TestClient(app)

def test_root():
    res = client.get("/")
    print(res.json())
    assert res.json().get("message") == "Bind mount is now working"
    assert res.status_code == 200
    
def test_create_user():
    res = client.post("/users/", json={"email": "test@example.com", "password": "password123"})
    print(res.json())
    assert res.status_code == 201
