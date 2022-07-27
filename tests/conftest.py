from os import environ

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.database.db import get_db
from app.main import app
import pytest

@pytest.fixture(scope="module")
def client():
    test_client = TestClient(app)
    yield test_client
SQLALCHEMY_DATABASE_URL = f'postgresql://{environ.get("POSTGRES_USER")}:{environ.get("POSTGRES_PASSWORD")}@{environ.get("POSTGRES_HOST")}:5432/{environ.get("POSTGRES_DB")}'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db
