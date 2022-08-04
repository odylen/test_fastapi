from typing import Union, List

from pydantic import BaseModel


class WorkingHours(BaseModel):
    week_day: int
    opening_hours: str


class ShopBase(BaseModel):
    title: str
    address: str
    latitude: float
    longitude: float
    images: List[str]
    open_days: List[WorkingHours]


class Shop(ShopBase):
    id: int

    class Config:
        orm_mode = True


class ShopEdit(BaseModel):
    id: int
    title: str = None
    address: str = None
    latitude: float = None
    longitude: float = None
    images: List[str] = None
    open_days: List[WorkingHours] = None

    class Config:
        orm_mode = True
