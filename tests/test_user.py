from datetime import datetime, timedelta

import pytest as pytest
from fastapi import status
from fastapi.testclient import TestClient

from app import schemas
from app.database import models
from app.database.db import get_db
from app.database.queries import PhoneCode, User
from app.settings import settings
from tests.conftest import override_get_db

db = next(override_get_db())


class TestUser:
    @pytest.fixture()
    def admin_token(self, client: TestClient):
        db_user = User.create_user(
            schemas.UserBase(
                phone="345",
            ),
            db,
            is_admin=True,
        )
        expire = datetime.utcnow() + timedelta(minutes=settings.sms_code_expire_minutes)
        PhoneCode.create_phone_code(phone="345", code="12345", expire=expire, db=db)
        response = client.post(
            "/api/auth/login", json={"phone": "345", "code": "12345"}
        )
        yield response.json()["access_token"]
        db.delete(db_user)
        db.commit()

    @pytest.fixture()
    def user_token(self, client: TestClient):
        db_user = User.create_user(
            schemas.UserBase(
                phone="3445",
            ),
            db,
        )
        expire = datetime.utcnow() + timedelta(minutes=settings.sms_code_expire_minutes)
        PhoneCode.create_phone_code(phone="3445", code="12345", expire=expire, db=db)
        response = client.post(
            "/api/auth/login", json={"phone": "3445", "code": "12345"}
        )
        yield response.json()["access_token"]
        db.delete(db_user)
        db.commit()

    def test_get(self, client: TestClient, admin_token):
        response = client.get("/api/user/", headers={"Authorization": admin_token})
        print(response.text)
        assert response.status_code == status.HTTP_200_OK
        assert "phone" in response.json().keys()

    def test_get_admin_not_found(self, client: TestClient, admin_token):
        response = client.get(
            "/api/user/",
            headers={"Authorization": admin_token},
            params={"user_id": 245235},
        )
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_get_not_admin(self, client: TestClient, user_token):
        response = client.get(
            "/api/user/",
            headers={"Authorization": user_token},
            params={"user_id": 245235},
        )
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_edit_user(self, client: TestClient, user_token):
        response = client.put(
            "/api/user/",
            headers={"Authorization": user_token},
            json={"name": "sddddd"},
        )
        assert response.status_code == status.HTTP_200_OK
        assert "name" in response.json().keys()
        assert response.json()["name"] == "sddddd"

    def test_all_users(self, client: TestClient, user_token, admin_token):
        response = client.get(
            "/api/user/all",
            headers={"Authorization": admin_token},
        )
        assert response.status_code == status.HTTP_200_OK
        assert len(response.json()['items']) > 0
