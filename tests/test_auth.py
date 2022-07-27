from datetime import datetime, timedelta

from fastapi import status
from fastapi.testclient import TestClient

from app.database import models
from app.database.db import get_db
from app.database.queries import PhoneCode
from app.settings import settings
from tests.conftest import override_get_db

db = next(override_get_db())


class TestAuth:

    def test_hello(self, client: TestClient):
        response = client.get(
            "/",
        )
        assert response.status_code == status.HTTP_200_OK
        assert "message" in response.json().keys()

    def test_sms(self, client: TestClient):
        response = client.post(
            "/api/auth/send_code",
            params={
                "phone": "12345678"
            }
        )
        assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR

    def test_login(self, client: TestClient):
        expire = datetime.utcnow() + timedelta(minutes=settings.sms_code_expire_minutes)
        PhoneCode.create_phone_code(phone="1111", code="12345", expire=expire, db=db)
        response = client.post(
            "/api/auth/login",
            json={
                "phone": "1111",
                "code": "12345"
            }
        )
        assert response.status_code == status.HTTP_200_OK
        assert "access_token" in response.json().keys()
        db_phone_code = (
            db.query(models.PhoneCode)
                .filter(models.PhoneCode.phone == "1111", models.PhoneCode.code == "12345")
                .first()
        )
        assert db_phone_code is None

    def test_login_wrong_code(self, client: TestClient):
        expire = datetime.utcnow() + timedelta(minutes=settings.sms_code_expire_minutes)
        PhoneCode.create_phone_code(phone="1111", code="12345", expire=expire, db=db)
        response = client.post(
            "/api/auth/login",
            json={
                "phone": "1111",
                "code": "123"
            }
        )
        db.query(models.PhoneCode).filter(models.PhoneCode.phone == "1111", models.PhoneCode.code == "12345").delete()
        db.commit()
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_login_expired_code(self, client: TestClient):
        expire = datetime.utcnow() - timedelta(minutes=settings.sms_code_expire_minutes)
        PhoneCode.create_phone_code(phone="1111", code="12345", expire=expire, db=db)
        response = client.post(
            "/api/auth/login",
            json={
                "phone": "1111",
                "code": "12345"
            }
        )
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
