import enum

from sqlalchemy import Boolean, Column, Integer, String, DateTime, ForeignKey, Enum
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

class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True)
    phone = Column(String, unique=True, index=True)
    name = Column(String)
    family = Column(String)
    patronymic = Column(String)
    type = Column(Enum(AccountType), default=AccountType.USER)

    bonus_card = relationship("BonusCard")


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
