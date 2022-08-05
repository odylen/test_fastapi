import os.path

import aiofiles as aiofiles
from fastapi import APIRouter, Depends, status, UploadFile, File
from fastapi_pagination import Page, paginate

from app.api.common.exceptions import not_admin_exception
from app.api.common.schemas import RequestStatus
from app.api.static.exceptions import invalid_file_exception
from app.api.static.helpers import generate_unique_filename, list_all_files
from app.api.static.schemas import FileUpload
from app.middleware.auth import is_admin

router = APIRouter(prefix="/static", tags=["static"])


@router.post("", response_model=FileUpload)
async def upload_file(
    filename: str = None,
    is_user_admin: bool = Depends(is_admin),
    in_file: UploadFile = File(...),
):
    if not is_user_admin:
        raise not_admin_exception
    fs = await in_file.read()
    print(in_file.content_type)
    if 'image' not in in_file.content_type:
        raise invalid_file_exception
    if not filename:
        filename = generate_unique_filename("/static")
        filename += '.' + in_file.content_type.split('/')[-1]
    async with aiofiles.open(os.path.join("/static/", filename), "wb") as out_file:
        content = fs
        await out_file.write(content)

    return FileUpload(filename=filename)


@router.delete("", response_model=RequestStatus)
async def delete_file(filename: str,   is_user_admin: bool = Depends(is_admin)):
    if not is_user_admin:
        raise not_admin_exception
    os.remove(os.path.join("/static/", filename))
    return RequestStatus()


@router.get("/all", response_model=Page[str])
async def get_all_files(is_user_admin: bool = Depends(is_admin)):
    if not is_user_admin:
        raise not_admin_exception
    return paginate(list_all_files('/static'))
