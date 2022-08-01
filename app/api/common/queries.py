import datetime

from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.api.common.helpers import generate_code
from app.api.product.queries import Product
from app.api.user import schemas
from app.database import models
from app.database.models import AccountType
from app.api.common.exceptions import user_already_exists_exception
from app.settings import settings


class User:
    @staticmethod
    def get_user_by_id(user_id: int, db: Session):
        return db.query(models.User).filter(models.User.id == user_id).first()

    @staticmethod
    def get_user_by_phone(phone: str, db: Session):
        return db.query(models.User).filter(models.User.phone == phone).first()

    @staticmethod
    def get_user_favorites(user_id: int, db: Session):

        return [el.id for el in db.query(models.User).filter(models.User.id == user_id).first().favorite_products]

    @staticmethod
    def create_user(user: schemas.UserBase, db: Session, is_admin: bool = False):
        try:
            db_user = models.User(**user.dict())
            if is_admin:
                db_user.type = AccountType.ADMIN
            db.add(db_user)
            card_code = generate_code(settings.card_code_length)
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
        db_user: models.User = (
            db.query(models.User).filter(models.User.id == user.id).first()
        )
        for key, value in user.dict().items():
            if value:
                setattr(db_user, key, value)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user

    @staticmethod
    def add_to_favorites(user_id: int, product_id, db: Session) -> models.User:
        db_user: models.User = (
            db.query(models.User).filter(models.User.id == user_id).first()
        )
        db_user.favorite_products.append(Product.get_product_by_id(product_id, db))

        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
