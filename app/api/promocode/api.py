from fastapi import APIRouter, Depends, status
from fastapi_pagination import Page
from sqlalchemy.orm import Session
from fastapi_pagination.ext.sqlalchemy import paginate

from app.api.promocode import schemas
from app.api.promocode.exceptions import promocode_not_found_exception, invalid_promocode_exception
from app.api.promocode.queries import Promocode
from app.api.common.schemas import RequestStatus
from app.database import models
from app.database.db import get_db
from app.api.common.exceptions import not_admin_exception
from app.database.models import DiscountType
from app.middleware.auth import is_admin

router = APIRouter(prefix="/promocode", tags=["promocode"])


@router.post("", status_code=status.HTTP_200_OK, response_model=schemas.Promocode)
def add_promocode(
    promocode: schemas.PromocodeBase,
    is_user_admin: bool = Depends(is_admin),
    db: Session = Depends(get_db),
):
    if not is_user_admin:
        raise not_admin_exception
    if promocode.type == DiscountType.PERCENT and promocode.amount > 1:
        raise invalid_promocode_exception
    return Promocode.create_promocode(promocode, db)


@router.delete("", status_code=status.HTTP_200_OK, response_model=RequestStatus)
def delete_promocode(
    promocode_id: int,
    is_user_admin: bool = Depends(is_admin),
    db: Session = Depends(get_db),
):
    if not is_user_admin:
        raise not_admin_exception
    promocode_db = Promocode.get_promocode_by_id(promocode_id, db)
    if not promocode_db:
        raise promocode_not_found_exception
    Promocode.delete_promocode(promocode_id, db)
    return RequestStatus()


@router.get(
    "/all",
    status_code=status.HTTP_200_OK,
    response_model=Page[schemas.Promocode],
)
def get_all_campaigns(
    is_user_admin: bool = Depends(is_admin),
    db: Session = Depends(get_db),
):
    if not is_user_admin:
        raise not_admin_exception
    return paginate(db.query(models.Promocode))
