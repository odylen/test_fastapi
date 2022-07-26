import datetime
from typing import List

from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.api.common.helpers import generate_code
from app.api.product.queries import Product
from app.api.promocode.queries import Promocode
from app.api.user import schemas
from app.database import models
from app.database.models import AccountType
from app.api.common.exceptions import user_already_exists_exception
from app.settings import settings


class User:
    @staticmethod
    def get_user_by_id(user_id: int, db: Session) -> models.User:
        return db.query(models.User).filter(models.User.id == user_id).first()

    @staticmethod
    def get_user_by_phone(phone: str, db: Session):
        return db.query(models.User).filter(models.User.phone == phone).first()

    @staticmethod
    def get_user_favorites(user_id: int, db: Session):

        return [
            el.id
            for el in db.query(models.User)
            .filter(models.User.id == user_id)
            .first()
            .favorite_products
        ]

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
            cart = models.Cart()
            db_user.cart = cart
            db.add(cart)
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

    @staticmethod
    def delete_from_favorites(user_id: int, product_id, db: Session) -> models.User:
        db_user: models.User = (
            db.query(models.User).filter(models.User.id == user_id).first()
        )
        db_user.favorite_products.remove(Product.get_product_by_id(product_id, db))

        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user

    @staticmethod
    def add_to_cart(user_id: int, product_id: int, db: Session) -> models.Cart:
        db_user: models.User = (
            db.query(models.User).filter(models.User.id == user_id).first()
        )
        db_cart_item: models.CartItem = (
            db.query(models.CartItem)
            .filter(
                models.CartItem.cart_id == db_user.cart.id,
                models.CartItem.product_id == product_id,
            )
            .first()
        )

        if not db_cart_item:
            db_cart_item = models.CartItem(
                product_id=product_id, cart_id=db_user.cart.id, amount=1
            )
        else:
            db_cart_item.amount += 1
        db.add(db_cart_item)
        db.commit()
        db.refresh(db_user)
        return db_user.cart

    @staticmethod
    def remove_from_cart(user_id: int, product_id: int, db: Session) -> models.Cart:
        db_user: models.User = (
            db.query(models.User).filter(models.User.id == user_id).first()
        )
        db_cart_item: models.CartItem = (
            db.query(models.CartItem)
            .filter(
                models.CartItem.cart_id == db_user.cart.id,
                models.CartItem.product_id == product_id,
            )
            .first()
        )

        if db_cart_item:
            if db_cart_item.amount > 0:
                db_cart_item.amount -= 1
            else:
                db.delete(db_cart_item)
        db.commit()
        db.refresh(db_user)
        return db_user.cart

    @staticmethod
    def get_cart(user_id: int, db: Session) -> models.Cart:
        db_user: models.User = (
            db.query(models.User).filter(models.User.id == user_id).first()
        )
        return db_user.cart

    @staticmethod
    def add_cart_promocode(promocode_id: int, user_id: int, db: Session) -> models.Cart:
        db_user: models.User = (
            db.query(models.User).filter(models.User.id == user_id).first()
        )
        promocode = Promocode.get_promocode_by_id(promocode_id, db)
        db_user.cart.promocode = promocode
        db.commit()
        db.refresh(db_user)
        return db_user.cart

    @staticmethod
    def delete_cart_promocode(user_id: int, db: Session) -> models.Cart:
        db_user: models.User = (
            db.query(models.User).filter(models.User.id == user_id).first()
        )
        db_user.cart.promocode = None
        db.commit()
        db.refresh(db_user)
        return db_user.cart

    @staticmethod
    def delete_all_cart(user_id: int, db: Session) -> models.Cart:
        db_user: models.User = (
            db.query(models.User).filter(models.User.id == user_id).first()
        )
        print(db_user.cart.products)
        for cart_item in db_user.cart.products:
            db.delete(cart_item)


        db.commit()
        db.refresh(db_user)
        return db_user.cart

    @staticmethod
    def add_address(user_id: int, address: str, db: Session) -> models.DeliveryAddress:
        db_user: models.User = (
            db.query(models.User).filter(models.User.id == user_id).first()
        )
        delivery_address = models.DeliveryAddress(address=address)
        db_user.delivery_addresses.append(delivery_address)
        db.add(delivery_address)
        db.commit()
        db.refresh(delivery_address)
        return delivery_address
