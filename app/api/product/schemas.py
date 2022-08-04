from typing import Union, List

from pydantic import BaseModel

from app.api.categories.schemas import Category


class ProductCategory(BaseModel):
    id: int

    class Config:
        orm_mode = True


class ProductBase(BaseModel):
    id: int
    title: str = None
    price: float = None
    categories: List[ProductCategory] = None
    favorite: bool = False

    class Config:
        orm_mode = True


class Product(ProductBase):
    description: str = None
    images_paths: List[str] = None
    nutritional_value: str = None
    constituents_descr: str = None
    weight: str = None

    class Config:
        orm_mode = True


class ProductAdd(BaseModel):
    title: str
    description: str
    iconpath: str
    price: float
    images_paths: List[str]
    categories: List[int]
    nutritional_value: str
    constituents_descr: str
    weight: str

    class Config:
        orm_mode = True


class ProductEdit(ProductBase):
    id: int
    title: Union[str, None] = None
    description: str = None
    iconpath: str = None
    price: float = None
    images_paths: List[str] = None
    categories: List[int] = None
    nutritional_value: str = None
    constituents_descr: str = None
    weight: str = None

    class Config:
        orm_mode = True
