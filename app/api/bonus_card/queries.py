from sqlalchemy.orm import Session

from app.api.bonus_card import schemas
from app.api.common.helpers import generate_code
from app.database import models
from app.settings import settings


class BonusCard:
    @staticmethod
    def get_card_by_id(card_id: int, db: Session) -> schemas.BonusCard:
        return db.query(models.BonusCard).filter(models.BonusCard.id == card_id).first()

    @staticmethod
    def create_bonus_card(user_id: int, db: Session) -> models.BonusCard:
        card_code = generate_code(settings.card_code_length)
        db_bonus_card = models.BonusCard(user_id=user_id, code=card_code)
        db.add(db_bonus_card)
        db.commit()
        db.refresh(db_bonus_card)
        return db_bonus_card

    @staticmethod
    def edit_bonus_card(card_id: int, user_id: int, code: str, db: Session) -> schemas.BonusCard:
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
