import enum

from sqlalchemy import (
    Boolean,
    Column,
    Integer,
    String,
    DateTime,
    ForeignKey,
    Enum,
    Table,
    ARRAY,
    JSON,
    Float, func,
)
from sqlalchemy.orm import relationship

from .db import Base


class AccountType(enum.Enum):
    ADMIN = 1
    USER = 2
    DELETED = 3


class BonusCard(Base):
    __tablename__ = "bonus_card2"

    code = Column(String)
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.id"))


favorite_product_association = Table(
    "favorite_product_association",
    Base.metadata,
    Column("user_id", ForeignKey("user.id")),
    Column("product_id", ForeignKey("product.id")),
)


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True)
    phone = Column(String, unique=True, index=True)
    name = Column(String)
    family = Column(String)
    patronymic = Column(String)
    type = Column(Enum(AccountType), default=AccountType.USER)
    cart = relationship("Cart", back_populates="user", uselist=False)

    bonus_card = relationship("BonusCard")
    delivery_addresses = relationship("DeliveryAddress")
    favorite_products = relationship("Product", secondary=favorite_product_association)


class DeliveryAddress(Base):
    __tablename__ = "delivery_address"

    id = Column(Integer, primary_key=True, index=True)
    address = Column(String)
    user_id = Column(Integer, ForeignKey("user.id"))


class PhoneCode(Base):
    __tablename__ = "phone_code"

    id = Column(Integer, primary_key=True, index=True)
    phone = Column(String, index=True)
    code = Column(String)
    expire = Column(DateTime)
    confirmed = Column(Boolean, default=False)


class Campaign(Base):
    __tablename__ = "campaign"

    id = Column(Integer, primary_key=True, index=True)
    is_active = Column(Boolean)
    title = Column(String)
    subtitle = Column(String)
    attention_text = Column(String)
    description = Column(String)
    type = Column(String)
    iconpath = Column(String)
    imagepath = Column(String)
    sort = Column(Integer)


product_category_association = Table(
    "product_category_association",
    Base.metadata,
    Column("product_id", ForeignKey("product.id")),
    Column("category_id", ForeignKey("category.id")),
)


class Product(Base):
    __tablename__ = "product"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String)
    price = Column(Float)
    iconpath = Column(String)
    images_paths_json = Column(ARRAY(String))
    nutritional_value_json = Column(String)
    constituents_descr = Column(String)
    weight = Column(String)

    categories_json = relationship("Category", secondary=product_category_association)


class Category(Base):
    __tablename__ = "category"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)


class Bakery(Base):
    __tablename__ = "bakery"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    address = Column(String)
    latitude = Column(Float)
    longitude = Column(Float)
    images = Column(ARRAY(String))
    open_days = Column(JSON)


class DeliveryOrder(Base):
    __tablename__ = "delivery_order"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.id"))
    bakery_id = Column(Integer, ForeignKey("bakery.id"))
    delivery_address_id = Column(Integer, ForeignKey("delivery_address.id"))
    products_ids = Column(ARRAY(Integer))
    comment = Column(String)


class OrderType(enum.Enum):
    DELIVERY = 1
    PICKUP = 2


class OrderStatus(enum.Enum):
    PAYMENT = 1
    PAID = 2
    DONE = 2


class Order(Base):
    __tablename__ = "order"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.id"))
    type = Column(Enum(OrderType))
    status = Column(Enum(OrderStatus), default=OrderStatus.PAYMENT)
    total = Column(Float)
    bakery_id = Column(Integer, ForeignKey("bakery.id"))
    delivery_address_id = Column(Integer, ForeignKey("delivery_address.id"))
    payment_link = Column(String)
    comment = Column(String)
    cart = Column(JSON)
    time_created = Column(DateTime(timezone=True), server_default=func.now())


class DiscountType(enum.Enum):
    PERCENT = 1
    ABSOLUTE = 2


class Promocode(Base):
    __tablename__ = "promocode"

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String)
    type = Column(Enum(DiscountType))
    amount = Column(Float)
    cart = relationship("Cart", back_populates="promocode")

class CartItem(Base):
    __tablename__ = "cart_item"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("product.id"))
    cart_id = Column(Integer, ForeignKey("cart.id"))
    amount = Column(Integer)

    product = relationship("Product")
    cart = relationship("Cart")


class Cart(Base):
    __tablename__ = "cart"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.id"))
    promocode_id = Column(Integer, ForeignKey("promocode.id"))
    total = Column(Integer)

    products = relationship("CartItem")
    user = relationship("User", back_populates="cart")
    promocode = relationship("Promocode", back_populates="cart")
