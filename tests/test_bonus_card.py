from datetime import datetime, timedelta

import pytest as pytest
from fastapi import status
from fastapi.testclient import TestClient

from app import schemas
from app.database import models
from app.database.db import get_db
from app.database.queries import PhoneCode, User, BonusCard
from app.settings import settings
from tests.conftest import override_get_db

db = next(override_get_db())


class TestBonusCard:
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

    def test_add_card(self, client: TestClient, user_token):
        response = client.post(
            "/api/bonus_card/",
            headers={"Authorization": user_token},
            json={"name": "sddddd"},
        )
        assert response.status_code == status.HTTP_200_OK
        assert "code" in response.json().keys()

    def test_edit_card(self, client: TestClient, admin_token, user_token):
        response = client.post(
            "/api/bonus_card/",
            headers={"Authorization": user_token},
            json={"name": "sddddd"},
        )
        card_id = response.json()['id']
        response = client.put(
            "/api/bonus_card/",
            headers={"Authorization": admin_token},
            params={"card_id": card_id,
                    "card_code": "sddddd"},
        )
        assert response.status_code == status.HTTP_200_OK
        assert "code" in response.json().keys()
        assert response.json()["code"] == "sddddd"

    def test_delete_card(self, client: TestClient, admin_token, user_token):
        response = client.post(
            "/api/bonus_card/",
            headers={"Authorization": user_token},
            json={"name": "sddddd"},
        )
        card_id = response.json()['id']
        response = client.delete(
            "/api/bonus_card/",
            headers={"Authorization": admin_token},
            params={"card_id": card_id},
        )
        assert response.status_code == status.HTTP_200_OK
        db_card = BonusCard.get_card_by_id(card_id, db)
        assert db_card is None

    def test_all_bonus(self, client: TestClient, user_token, admin_token):
        response = client.get(
            "/api/bonus_card/all",
            headers={"Authorization": admin_token},
        )
        assert response.status_code == status.HTTP_200_OK
        assert len(response.json()['items']) > 0
