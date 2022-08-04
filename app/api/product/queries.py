from sqlalchemy.orm import Session

from app.api.categories.queries import Category
from app.api.product import schemas
from app.database import models


class Product:
    @staticmethod
    def get_product_by_id(product_id: int, db: Session) -> models.Product:
        return db.query(models.Product).filter(models.Product.id == product_id).first()

    @staticmethod
    def create_product(product: schemas.ProductAdd, db: Session) -> models.Product:
        product_dict = product.dict()
        categories = product_dict["categories"]
        del product_dict["categories"]
        db_product = models.Product(**product_dict)
        db.add(db_product)
        for category in categories:
            db_product.categories.append(Category.get_category_by_id(category, db))
        db.commit()
        db.refresh(db_product)
        return db_product

    @staticmethod
    def edit_product(product: schemas.ProductEdit, db: Session) -> models.Product:
        db_product: models.Product = (
            db.query(models.Product).filter(models.Product.id == product.id).first()
        )
        for key, value in product.dict().items():
            if value:
                if key == "categories":
                    db_product.categories = []
                    for category in value:
                        db_product.categories.append(Category.get_category_by_id(category, db))
                else:
                    setattr(db_product, key, value)
        db.add(db_product)
        db.commit()
        db.refresh(db_product)
        return db_product

    @staticmethod
    def delete_product(product_id: int, db: Session):
        db.query(models.Product).filter(models.Product.id == product_id).delete()
        db.commit()
