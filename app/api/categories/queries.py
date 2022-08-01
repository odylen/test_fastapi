from sqlalchemy.orm import Session

from app.api.categories import schemas
from app.database import models


class Category:
    @staticmethod
    def get_category_by_id(category_id: int, db: Session) -> models.Category:
        return (
            db.query(models.Category).filter(models.Category.id == category_id).first()
        )

    @staticmethod
    def create_category(category: schemas.CategoryBase, db: Session) -> models.Category:
        db_category = models.Category(**category.dict())
        db.add(db_category)
        db.commit()
        db.refresh(db_category)
        return db_category

    @staticmethod
    def edit_category(category: schemas.Category, db: Session) -> models.Category:
        db_category: models.Category = (
            db.query(models.Category).filter(models.Category.id == category.id).first()
        )
        for key, value in category.dict().items():
            if value:
                setattr(db_category, key, value)
        db.add(db_category)
        db.commit()
        db.refresh(db_category)
        return db_category

    @staticmethod
    def delete_category(category_id: int, db: Session):
        db.query(models.Category).filter(models.Category.id == category_id).delete()
        db.commit()
