from datetime import datetime, timedelta

import pytest as pytest
from fastapi import status
from fastapi.testclient import TestClient

from app.api.auth.queries import PhoneCode
from app.api.campaign.queries import Campaign
from app.api.common.queries import User
from app.api.user import schemas
from app.database import models
from app.database.db import get_db
from app.settings import settings
from tests.conftest import override_get_db

db = next(override_get_db())


class TestCampaign:
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

    def test_add_card(self, client: TestClient, admin_token):
        response = client.post(
            "/api/campaign/",
            headers={"Authorization": admin_token},
            json={
                "title": "sddddd",
                "type": "sddddd",
                "iconpath": "sddddd",
                "is_active": False,
                "imagepath": "sds",
                "subtitle": "sds",
                "attention_text": "sds",
                "description": "sds",
                "sort": 234,
            },
        )
        assert response.status_code == status.HTTP_200_OK
        assert "title" in response.json().keys()
        assert response.json()["title"] == "sddddd"

    def test_edit_campaign(self, client: TestClient, admin_token, user_token):
        response = client.post(
            "/api/campaign/",
            headers={"Authorization": admin_token},
            json={
                "title": "sddddd",
                "type": "sddddd",
                "iconpath": "sddddd",
                "is_active": False,
                "imagepath": "sds",
                "subtitle": "sds",
                "attention_text": "sds",
                "description": "sds",
                "sort": 234,
            },
        )

        campaign_id = response.json()["id"]
        response = client.put(
            "/api/campaign/",
            headers={"Authorization": admin_token},
            json={"id": campaign_id, "iconpath": "dsfsdfsd"},
        )
        assert response.status_code == status.HTTP_200_OK
        assert "iconpath" in response.json().keys()
        assert response.json()["iconpath"] == "dsfsdfsd"

    def test_delete_campaign(self, client: TestClient, admin_token, user_token):
        response = client.post(
            "/api/campaign/",
            headers={"Authorization": admin_token},
            json={
                "title": "sddddd",
                "type": "sddddd",
                "iconpath": "sddddd",
                "is_active": False,
                "imagepath": "sds",
                "subtitle": "sds",
                "attention_text": "sds",
                "description": "sds",
                "sort": 234,
            },
        )

        campaign_id = response.json()["id"]
        response = client.delete(
            "/api/campaign/",
            headers={"Authorization": admin_token},
            params={"campaign_id": campaign_id},
        )
        assert response.status_code == status.HTTP_200_OK
        db_campaign = Campaign.get_campaign_by_id(campaign_id, db)
        assert db_campaign is None

    def test_all_campaign(self, client: TestClient, user_token, admin_token):
        response = client.post(
            "/api/campaign/",
            headers={"Authorization": admin_token},
            json={
                "title": "sddddd",
                "type": "sddddd",
                "iconpath": "sddddd",
                "is_active": False,
                "imagepath": "sds",
                "subtitle": "sds",
                "attention_text": "sds",
                "description": "sds",
                "sort": 234,
            },
        )

        response = client.get(
            "/api/campaign/all",
        )
        assert response.status_code == status.HTTP_200_OK
        assert len(response.json()) > 0
