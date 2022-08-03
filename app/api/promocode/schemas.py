from typing import Union

from pydantic import BaseModel

from app.database.models import DiscountType


class PromocodeBase(BaseModel):
    code: str
    type: DiscountType
    amount: float


class Promocode(PromocodeBase):
    id: int

    class Config:
        orm_mode = True
