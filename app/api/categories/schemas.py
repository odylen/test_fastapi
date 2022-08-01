from typing import Union

from pydantic import BaseModel


class CategoryBase(BaseModel):
    title: str


class Category(CategoryBase):
    id: int

    class Config:
        orm_mode = True
