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

router = APIRouter(prefix="/shop", tags=["shop"])


@router.get(
    "",
    status_code=status.HTTP_200_OK,
    response_model=schemas.Shop,
)
def get_shop(
    shop_id: int,
    db: Session = Depends(get_db),
):
    bakery_db = Bakery.get_bakery_by_id(shop_id, db)
    if not bakery_db:
        raise bakery_not_found_exception
    return bakery_db


@router.post("", status_code=status.HTTP_200_OK, response_model=schemas.Shop)
def add_shop(
    shop: schemas.ShopBase,
    is_user_admin: bool = Depends(is_admin),
    db: Session = Depends(get_db),
):
    if not is_user_admin:
        raise not_admin_exception
    return Bakery.create_bakery(shop, db)


@router.put("", status_code=status.HTTP_200_OK, response_model=schemas.Shop)
def edit_shop(
    shop: schemas.ShopEdit,
    is_user_admin: bool = Depends(is_admin),
    db: Session = Depends(get_db),
):
    if not is_user_admin:
        raise not_admin_exception
    bakery_db = Bakery.get_bakery_by_id(shop.id, db)
    if not bakery_db:
        raise bakery_not_found_exception
    return Bakery.edit_bakery(shop, db)


@router.delete("", status_code=status.HTTP_200_OK, response_model=RequestStatus)
def delete_shop(
    shop_id: int,
    is_user_admin: bool = Depends(is_admin),
    db: Session = Depends(get_db),
):
    if not is_user_admin:
        raise not_admin_exception
    bakery_db = Bakery.get_bakery_by_id(shop_id, db)
    if not bakery_db:
        raise bakery_not_found_exception
    Bakery.delete_bakery(bakery_db, db)
    return RequestStatus()


@router.get(
    "/all",
    status_code=status.HTTP_200_OK,
    response_model=List[schemas.Shop],
)
def get_all_shops(
    db: Session = Depends(get_db),
):
    return db.query(models.Bakery).all()
