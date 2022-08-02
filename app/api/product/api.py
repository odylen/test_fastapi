from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from starlette import status

from app.api.common.queries import User
from app.api.product import schemas
from app.api.product.exceptions import product_not_found_exception
from app.api.product.queries import Product
from app.api.common.schemas import RequestStatus
from app.database import models
from app.database.db import get_db
from app.api.common.exceptions import not_admin_exception
from app.middleware.auth import is_admin, is_authenticated

router = APIRouter(prefix="/product", tags=["product"])


@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    response_model=schemas.Product,
)
def get_product(
    product_id: int,
    requested_user_id: int = Depends(is_authenticated),
    db: Session = Depends(get_db),
):
    product_db = Product.get_product_by_id(product_id, db)
    if not product_db:
        raise product_not_found_exception
    if product_db.id in User.get_user_favorites(user_id=requested_user_id, db=db):
        resp = schemas.Product.from_orm(product_db)
        resp.favorite = True
        return resp

    return product_db


@router.post("/", status_code=status.HTTP_200_OK, response_model=schemas.Product)
def add_product(
    product: schemas.ProductAdd,
    is_user_admin: bool = Depends(is_admin),
    db: Session = Depends(get_db),
):
    if not is_user_admin:
        raise not_admin_exception
    created = Product.create_product(product, db)
    print(created.categories_json)
    return created


@router.put("/", status_code=status.HTTP_200_OK, response_model=schemas.Product)
def edit_product(
    product: schemas.ProductEdit,
    is_user_admin: bool = Depends(is_admin),
    db: Session = Depends(get_db),
):
    if not is_user_admin:
        raise not_admin_exception
    product_db = Product.get_product_by_id(product.id, db)
    if not product_db:
        raise product_not_found_exception
    return Product.edit_product(product, db)


@router.delete("/", status_code=status.HTTP_200_OK, response_model=RequestStatus)
def delete_product(
    product_id: int,
    is_user_admin: bool = Depends(is_admin),
    db: Session = Depends(get_db),
):
    if not is_user_admin:
        raise not_admin_exception
    product_db = Product.get_product_by_id(product_id, db)
    if not product_db:
        raise product_not_found_exception
    Product.delete_product(product_id, db)
    return RequestStatus()


@router.get(
    "/all",
    status_code=status.HTTP_200_OK,
    response_model=List[schemas.ProductBase],
)
def get_all_products(
    requested_user_id: int = Depends(is_authenticated),
    db: Session = Depends(get_db),
):
    favorites = User.get_user_favorites(user_id=requested_user_id, db=db)
    product_list = []
    for product in db.query(models.Product).all():
        resp = schemas.ProductBase.from_orm(product)
        if product.id in favorites:
            resp.favorite = True
        product_list.append(resp)
    return product_list
