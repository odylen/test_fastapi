from typing import Union, List

from pydantic import BaseModel

from app.api.categories.schemas import Category


class FileUpload(BaseModel):
    filename: str
