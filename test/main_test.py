import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from ..app.database import Base
from ..app.main import app, get_db

SQLALCHEMY_DATABASE_URL = "postgresql://postgres:1234@localhost/test"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

def test_create_feedback():
    response = client.post(
        "/feedback/",
        json={"score": 5, "comment": "Great product!", "created_at": "2023-07-09T00:00:00"},
    )
    assert response.status_code == 200
    assert response.json()["score"] == 5
    assert response.json()["comment"] == "Great product!"
