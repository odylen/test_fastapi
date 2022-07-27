from typing import Union

from pydantic import BaseModel


class BonusCardBase(BaseModel):
    user_id: int = None
    code: str = None


class BonusCard(BonusCardBase):
    id: int

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str


class SendTokenResponse(BaseModel):
    code_id: str


class ValidateTokenResponse(BaseModel):
    code_id: str
    confirmed: bool


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
    # allows conversion between Pydantic and ORMs
    class Config:
        orm_mode = True


class UserEdit(BaseModel):
    id: Union[int, None] = None
    name: Union[str, None] = None
    family: Union[str, None] = None
    patronymic: Union[str, None] = None
    phone: Union[str, None] = None


class CampaignBase(BaseModel):
    id: int
    title: str = None
    type: str = None
    iconpath: str = None

    class Config:
        orm_mode = True


class Campaign(CampaignBase):
    is_active: bool = None
    imagepath: str = None
    subtitle: str = None
    attention_text: str = None
    description: str = None
    sort: int = None

    class Config:
        orm_mode = True


class CampaignAdd(BaseModel):
    title: str
    type: str
    iconpath: str
    is_active: bool
    imagepath: str
    subtitle: str
    attention_text: str
    description: str
    sort: int

    class Config:
        orm_mode = True


class CampaignEdit(CampaignBase):
    id: int
    title: Union[str, None] = None
    type: Union[str, None] = None
    iconpath: Union[str, None] = None
    is_active: Union[bool, None] = None
    imagepath: Union[str, None] = None
    subtitle: Union[str, None] = None
    attention_text: Union[str, None] = None
    description: Union[str, None] = None
    sort: Union[int, None] = None

    class Config:
        orm_mode = True
