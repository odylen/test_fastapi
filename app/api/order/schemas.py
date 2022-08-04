import datetime
from typing import Union, List

from pydantic import BaseModel

from app.database.models import OrderType, OrderStatus


class OrderCreate(BaseModel):
    type: OrderType
    bakery_id: int = None
    delivery_address_id: int = None
    comment: str = None

    class Config:
        orm_mode = True


class Order(BaseModel):
    id: int
    type: OrderType
    status: OrderStatus
    payment_link: str
    cart: dict
    time_created: datetime.datetime
    comment: str = None
    bakery_id: int = None
    delivery_address_id: int = None

    class Config:
        orm_mode = True


class OrderStatus(BaseModel):
    id: int
    status: OrderStatus

    class Config:
        orm_mode = True
