from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from starlette import status

from app.api.bakery import schemas
from app.api.bakery.exceptions import bakery_not_found_exception
from app.api.bakery.queries import Bakery
from app.api.common.schemas import RequestStatus
from app.database import models
from app.database.db import get_db
from app.api.common.exceptions import not_admin_exception
from app.middleware.auth import is_admin

router = APIRouter(prefix="/bakery", tags=["bakery"])


@router.get(
    "",
    status_code=status.HTTP_200_OK,
    response_model=schemas.Bakery,
)
def get_bakery(
    bakery_id: int,
    db: Session = Depends(get_db),
):
    bakery_db = Bakery.get_bakery_by_id(bakery_id, db)
    if not bakery_db:
        raise bakery_not_found_exception
    return bakery_db


@router.post("", status_code=status.HTTP_200_OK, response_model=schemas.Bakery)
def add_bakery(
    bakery: schemas.BakeryBase,
    is_user_admin: bool = Depends(is_admin),
    db: Session = Depends(get_db),
):
    if not is_user_admin:
        raise not_admin_exception
    return Bakery.create_bakery(bakery, db)


@router.put("", status_code=status.HTTP_200_OK, response_model=schemas.Bakery)
def edit_bakery(
    bakery: schemas.BakeryEdit,
    is_user_admin: bool = Depends(is_admin),
    db: Session = Depends(get_db),
):
    if not is_user_admin:
        raise not_admin_exception
    bakery_db = Bakery.get_bakery_by_id(bakery.id, db)
    if not bakery_db:
        raise bakery_not_found_exception
    return Bakery.edit_bakery(bakery, db)


@router.delete("", status_code=status.HTTP_200_OK, response_model=RequestStatus)
def delete_bakery(
    bakery_id: int,
    is_user_admin: bool = Depends(is_admin),
    db: Session = Depends(get_db),
):
    if not is_user_admin:
        raise not_admin_exception
    bakery_db = Bakery.get_bakery_by_id(bakery_id, db)
    if not bakery_db:
        raise bakery_not_found_exception
    Bakery.delete_bakery(bakery_db, db)
    return RequestStatus()


@router.get(
    "/all",
    status_code=status.HTTP_200_OK,
    response_model=List[schemas.Bakery],
)
def get_all_bakeries(
    db: Session = Depends(get_db),
):
    return db.query(models.Bakery).all()
