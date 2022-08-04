import os.path
from pathlib import Path

import aiofiles as aiofiles
from fastapi import APIRouter, Depends, status, UploadFile, File

from app.api.common.schemas import RequestStatus
from app.api.static.schemas import FileUpload

router = APIRouter(prefix="/static", tags=["static"])


@router.post("", response_model=FileUpload)
async def upload_file(filename: str, in_file: UploadFile = File(...)):
    fs = await in_file.read()
    Path("/static").mkdir(parents=True, exist_ok=True)
    async with aiofiles.open(os.path.join("/static/", filename), "wb") as out_file:
        content = fs
        await out_file.write(content)

    return FileUpload(filename=filename)


@router.post("", response_model=RequestStatus)
async def delete_file(filename: str):
    os.remove(os.path.join("/static/", filename))
    return RequestStatus()
