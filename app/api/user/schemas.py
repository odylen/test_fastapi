from typing import Union

from pydantic import BaseModel



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
