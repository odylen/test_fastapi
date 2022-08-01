from typing import Union

from pydantic import BaseModel


class BonusCardBase(BaseModel):
    user_id: int = None
    code: str = None


class BonusCard(BonusCardBase):
    id: int

    class Config:
        orm_mode = True
