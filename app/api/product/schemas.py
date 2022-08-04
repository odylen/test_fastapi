from typing import Union, List

from pydantic import BaseModel



class ProductCategory(BaseModel):
    id: int

    class Config:
        orm_mode = True


class ProductBase(BaseModel):
    id: int
    title: str = None
    price: float = None
    iconpath: str = None
    categories: List[int] = None
    favorite: bool = False

    class Config:
        orm_mode = True


class Product(ProductBase):
    description: str = None
    images_paths: List[str] = None
    nutritional_value: str = None
    composition: List[str] = None
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
    composition: List[str]
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
    composition: List[str] = None
    weight: str = None

    class Config:
        orm_mode = True
