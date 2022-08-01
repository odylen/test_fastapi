import datetime

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.api.common.exceptions import user_already_exists_exception
from app.database import models


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
