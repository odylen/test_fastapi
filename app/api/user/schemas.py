from typing import Union, List

from pydantic import BaseModel

from app.api.categories.schemas import Category
from app.api.product.schemas import Product
from app.database.models import DiscountType


class UserBase(BaseModel):
    phone: str


class User(UserBase):
    id: int
    name: str = None
    family: str = None
    patronymic: str = None

    class Config:
        orm_mode = True


class UserResponse(BaseModel):
    id: int
    phone: str
    name: str = None
    family: str = None
    patronymic: str = None

    class Config:
        orm_mode = True


class UserEdit(BaseModel):
    id: Union[int, None] = None
    name: Union[str, None] = None
    family: Union[str, None] = None
    patronymic: Union[str, None] = None
    phone: Union[str, None] = None


class CartProduct(BaseModel):
    id: int
    title: str
    iconpath: str
    price: float

    class Config:
        orm_mode = True


class CartPosition(BaseModel):
    amount: int
    product: CartProduct

    class Config:
        orm_mode = True


class CartPromocode(BaseModel):
    code: str
    type: DiscountType
    amount: float

    class Config:
        orm_mode = True


class CartResp(BaseModel):
    id: int
    products: List[CartPosition]
    total: float
    promocode: CartPromocode = None

    class Config:
        orm_mode = True


class OptCartResp(BaseModel):
    success: bool = True
    cart: CartResp = None

    class Config:
        orm_mode = True


class DeliveryAddressBase(BaseModel):
    address: str


class DeliveryAddress(DeliveryAddressBase):
    id: int

    class Config:
        orm_mode = True
