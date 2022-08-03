from sqlalchemy.orm import Session

from app.api.promocode import schemas
from app.database import models


class Promocode:
    @staticmethod
    def get_promocode_by_id(promocode_id: int, db: Session) -> models.Campaign:
        return db.query(models.Promocode).filter(models.Promocode.id == promocode_id).first()
    @staticmethod
    def get_promocode_by_code(code: str, db: Session) -> models.Campaign:
        return db.query(models.Promocode).filter(models.Promocode.code == code).first()

    @staticmethod
    def create_promocode(promocode: schemas.PromocodeBase, db: Session) -> models.Promocode:
        db_promocode = models.Promocode(**promocode.dict())
        db.add(db_promocode)
        db.commit()
        db.refresh(db_promocode)
        return db_promocode

    @staticmethod
    def delete_promocode(promocode_id: int, db: Session):
        db.query(models.Promocode).filter(models.Promocode.id == promocode_id).delete()
        db.commit()
