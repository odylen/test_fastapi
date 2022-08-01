from typing import Union

from pydantic import BaseModel


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
