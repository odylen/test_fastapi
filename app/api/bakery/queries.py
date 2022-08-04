from sqlalchemy.orm import Session

from app.api.bakery import schemas
from app.database import models


class Bakery:
    @staticmethod
    def get_bakery_by_id(bakery_id: int, db: Session) -> models.Bakery:
        return db.query(models.Bakery).filter(models.Bakery.id == bakery_id).first()

    @staticmethod
    def create_bakery(bakery: schemas.ShopBase, db: Session) -> models.Bakery:
        db_bakery = models.Bakery(**bakery.dict())
        db.add(db_bakery)
        db.commit()
        db.refresh(db_bakery)
        return db_bakery

    @staticmethod
    def edit_bakery(bakery: schemas.ShopEdit, db: Session) -> models.Bakery:
        db_bakery: models.Bakery = (
            db.query(models.Bakery).filter(models.Bakery.id == bakery.id).first()
        )
        for key, value in bakery.dict().items():
            if value:
                setattr(db_bakery, key, value)
        db.add(db_bakery)
        db.commit()
        db.refresh(db_bakery)
        return db_bakery

    @staticmethod
    def delete_bakery(bakery_id: int, db: Session):
        db.query(models.Bakery).filter(models.Bakery.id == bakery_id).delete()
        db.commit()
