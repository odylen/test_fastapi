import datetime
import os
from typing import List

from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app import schemas
from app.database import models
from app.helpers.auth import get_password_hash, generate_code
from app.exceptions.user import user_already_exists_exception
from app.settings import CARD_CODE_LENGTH


class User:
    @staticmethod
    def get_user_by_id(id: int, db: Session):
        return db.query(models.User).filter(models.User.id == id).first()

    @staticmethod
    def get_user_by_phone(phone: str, db: Session):
        return db.query(models.User).filter(models.User.phone == phone).first()

    @staticmethod
    def create_user(user: schemas.UserBase, db: Session):
        try:
            user.password = get_password_hash(user.password)
            print(user.password)
            db_user = models.User(**user.dict())
            db.add(db_user)
            card_code = generate_code(CARD_CODE_LENGTH)
            bonus_card = models.BonusCard(code=card_code)
            db_user.bonus_card.append(bonus_card)
            db.add(bonus_card)
            db.commit()
            db.refresh(db_user)
            return db_user
        except IntegrityError:
            raise user_already_exists_exception

    @staticmethod
    def edit_user(user: schemas.UserEdit, db: Session) -> models.Campaign:
        db_user: models.User = db.query(models.User).filter(models.User.id == user.id).first()
        for key, value in user.dict().items():
            if value:
                if key == 'password':
                    value = get_password_hash(value)
                setattr(db_user, key, value)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user


class PhoneCode:

    @staticmethod
    def get_code_by_id(id: int, db: Session) -> models.PhoneCode:
        return db.query(models.PhoneCode).filter(models.PhoneCode.id == id).first()

    @staticmethod
    def confirm_phone(id: int, db: Session):
        db_phone_code: models.PhoneCode = db.query(models.PhoneCode).filter(models.PhoneCode.id == id).first()
        db_phone_code.confirmed = True
        db.commit()

    @staticmethod
    def create_phone_code(phone: str, code: str, expire: datetime.datetime, db: Session) -> models.PhoneCode:
        try:
            db_code = models.PhoneCode(phone=phone, code=code, expire=expire)
            db.add(db_code)
            db.commit()
            db.refresh(db_code)
            return db_code
        except IntegrityError:
            raise user_already_exists_exception


class BonusCard:
    @staticmethod
    def get_card_by_id(card_id: int, db: Session) -> schemas.BonusCard:
        return db.query(models.BonusCard).filter(models.BonusCard.id == card_id).first()

    @staticmethod
    def create_bonus_card(user_id: int, db: Session) -> models.BonusCard:
        card_code = generate_code(CARD_CODE_LENGTH)
        db_bonus_card = models.BonusCard(user_id=user_id, code=card_code)
        db.add(db_bonus_card)
        db.commit()
        db.refresh(db_bonus_card)
        return db_bonus_card

    @staticmethod
    def edit_bonus_card(card_id: int, user_id: int, code: str, db: Session):
        db_bonus_card: models.BonusCard = db.query(models.BonusCard).filter(models.BonusCard.id == card_id).first()
        if user_id:
            db_bonus_card.user = user_id
        if code:
            db_bonus_card.code = code
        db.commit()

        db.refresh(db_bonus_card)
        return db_bonus_card

    @staticmethod
    def delete_bonus_card(card_id: int, db: Session):
        db.query(models.BonusCard).filter(models.BonusCard.id == card_id).delete()
        db.commit()


class Campaign:
    @staticmethod
    def get_campaign_by_id(campaign_id: int, db: Session) -> models.Campaign:
        return db.query(models.Campaign).filter(models.Campaign.id == campaign_id).first()

    @staticmethod
    def create_campaign(campaign: schemas.CampaignAdd, db: Session) -> models.Campaign:
        db_campaign = models.Campaign(**campaign.dict())
        db.add(db_campaign)
        db.commit()
        db.refresh(db_campaign)
        return db_campaign

    @staticmethod
    def edit_campaign(campaign: schemas.Campaign, db: Session) -> models.Campaign:
        db_campaign: models.Campaign = db.query(models.Campaign).filter(models.Campaign.id == campaign.id).first()
        for key, value in campaign.dict().items():
            if value:
                setattr(db_campaign, key, value)
        db.add(db_campaign)
        db.commit()
        db.refresh(db_campaign)
        return db_campaign
    @staticmethod
    def delete_campaign(campaign_id: int, db: Session):
        db.query(models.Campaign).filter(models.Campaign.id == campaign_id).delete()
        db.commit()
