from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from starlette import status

from app.api.categories import schemas
from app.api.categories.exceptions import category_not_found_exception
from app.api.categories.queries import Category
from app.api.common.schemas import RequestStatus
from app.database import models
from app.database.db import get_db
from app.api.common.exceptions import not_admin_exception
from app.middleware.auth import is_admin

router = APIRouter(prefix="/category", tags=["category"])


@router.get(
    "",
    status_code=status.HTTP_200_OK,
    response_model=schemas.Category,
)
def get_category(
    category_id: int,
    db: Session = Depends(get_db),
):
    category_db = Category.get_category_by_id(category_id, db)
    if not category_db:
        raise category_not_found_exception
    return category_db


@router.post("", status_code=status.HTTP_200_OK, response_model=schemas.Category)
def add_category(
    category: schemas.CategoryBase,
    is_user_admin: bool = Depends(is_admin),
    db: Session = Depends(get_db),
):
    if not is_user_admin:
        raise not_admin_exception
    return Category.create_category(category, db)


@router.put("", status_code=status.HTTP_200_OK, response_model=schemas.Category)
def edit_campaign(
    category: schemas.Category,
    is_user_admin: bool = Depends(is_admin),
    db: Session = Depends(get_db),
):
    if not is_user_admin:
        raise not_admin_exception
    category_db = Category.get_category_by_id(category.id, db)
    if not category_db:
        raise category_not_found_exception
    return Category.edit_category(category, db)


@router.delete("", status_code=status.HTTP_200_OK, response_model=RequestStatus)
def delete_category(
    category_id: int,
    is_user_admin: bool = Depends(is_admin),
    db: Session = Depends(get_db),
):
    if not is_user_admin:
        raise not_admin_exception
    category_db = Category.get_category_by_id(category_id, db)
    if not category_db:
        raise category_not_found_exception
    Category.delete_category(category_id, db)
    return RequestStatus()


@router.get(
    "/all",
    status_code=status.HTTP_200_OK,
    response_model=List[schemas.Category],
)
def get_all_categories(
    db: Session = Depends(get_db),
):
    return db.query(models.Category).all()
