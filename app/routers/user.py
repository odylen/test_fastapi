from fastapi import APIRouter, status, Body, Depends
from fastapi_pagination import Page
from sqlalchemy.orm import Session

from app import schemas
from app.database import models
from app.database.db import get_db
from app.database.models import AccountType
from app.database.queries import User
from app.exceptions.user import user_not_found_exception, not_admin_exception
from app.middleware.auth import is_autheticated, is_admin
from fastapi_pagination.ext.sqlalchemy import paginate

router = APIRouter(prefix="/user", tags=["user"])

@router.get(
    "/", status_code=status.HTTP_200_OK, response_model=schemas.UserResponse
)
def get_user_by_id(
    user_id: int = None,
    requested_user_id: int = Depends(is_autheticated),
    is_user_admin: bool = Depends(is_admin),
    db: Session = Depends(get_db),
):
    if user_id and user_id != requested_user_id and not is_user_admin:
        raise not_admin_exception
    if not user_id:
        user_id = requested_user_id
    db_user = User.get_user_by_id(user_id, db)
    if not db_user:
        raise user_not_found_exception

    return db_user


@router.get(
    "/by_phone", status_code=status.HTTP_200_OK, response_model=schemas.UserResponse
)
def get_user_by_phone(
    user_phone: str,
    requested_user_id: int = Depends(is_autheticated),
    is_user_admin: bool = Depends(is_admin),
    db: Session = Depends(get_db),
):
    db_user = User.get_user_by_phone(user_phone, db)
    if not db_user:
        raise user_not_found_exception
    if db_user.id != requested_user_id and not is_user_admin:
        raise not_admin_exception
    return db_user


@router.put("/", status_code=status.HTTP_200_OK, response_model=schemas.UserResponse)
def edit_user(
    user: schemas.UserEdit,
    requested_user_id: int = Depends(is_autheticated),
    is_user_admin: bool = Depends(is_admin),
    db: Session = Depends(get_db),
):
    if user.id and user.id != requested_user_id and not is_user_admin:
        raise not_admin_exception
    if not user.id:
        user.id = requested_user_id
    db_user = User.get_user_by_id(user.id, db)
    if not db_user:
        raise user_not_found_exception

    return User.edit_user(user, db)


@router.get("/all", status_code=status.HTTP_200_OK, response_model=Page[schemas.UserResponse])
def get_all_users(
    is_user_admin: bool = Depends(is_admin), db: Session = Depends(get_db)
):
    if not is_user_admin:
        raise not_admin_exception
    return paginate(db.query(models.User).filter(models.User.type == AccountType.USER))
