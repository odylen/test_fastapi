from typing import List

from fastapi import APIRouter, status, Depends
from fastapi_pagination import Page
from sqlalchemy.orm import Session

from app.api.common.helpers import count_cart
from app.api.common.queries import User
from app.api.common.schemas import RequestStatus
from app.api.promocode.exceptions import promocode_not_found_exception
from app.api.promocode.queries import Promocode
from app.api.user import schemas
from app.api.user.schemas import CartResp, OptCartResp
from app.database import models
from app.database.db import get_db
from app.database.models import AccountType
from app.api.common.exceptions import user_not_found_exception, not_admin_exception
from app.middleware.auth import is_authenticated, is_admin
from fastapi_pagination.ext.sqlalchemy import paginate

router = APIRouter(prefix="/user", tags=["user"])


@router.get("/", status_code=status.HTTP_200_OK, response_model=schemas.UserResponse)
def get_user_by_id(
    user_id: int = None,
    requested_user_id: int = Depends(is_authenticated),
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
    requested_user_id: int = Depends(is_authenticated),
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
    requested_user_id: int = Depends(is_authenticated),
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


@router.get(
    "/all", status_code=status.HTTP_200_OK, response_model=Page[schemas.UserResponse]
)
def get_all_users(
    is_user_admin: bool = Depends(is_admin), db: Session = Depends(get_db)
):
    if not is_user_admin:
        raise not_admin_exception
    return paginate(db.query(models.User).filter(models.User.type == AccountType.USER))


@router.post(
    "/add_to_favorites", status_code=status.HTTP_200_OK, response_model=RequestStatus
)
def add_to_favorites(
    product_id: int,
    requested_user_id: int = Depends(is_authenticated),
    db: Session = Depends(get_db),
):
    User.add_to_favorites(requested_user_id, product_id, db)
    return RequestStatus()


@router.post("/cart/product", status_code=status.HTTP_200_OK, response_model=OptCartResp)
def add_to_cart(
    product_id: int,
    return_cart: bool = False,
    requested_user_id: int = Depends(is_authenticated),
    db: Session = Depends(get_db),
):
    cart = User.add_to_cart(requested_user_id, product_id, db)
    resp = OptCartResp()
    if return_cart:
        resp.cart = CartResp.from_orm(count_cart(cart))
    return resp


@router.delete("/cart/product", status_code=status.HTTP_200_OK, response_model=OptCartResp)
def delete_from_cart(
    product_id: int,
    return_cart: bool = False,
    requested_user_id: int = Depends(is_authenticated),
    db: Session = Depends(get_db),
):
    cart = User.remove_from_cart(requested_user_id, product_id, db)
    resp = OptCartResp()
    if return_cart:
        resp.cart = CartResp.from_orm(count_cart(cart))
    return resp


@router.delete("/cart/all", status_code=status.HTTP_200_OK, response_model=CartResp)
def delete_from_cart(
    requested_user_id: int = Depends(is_authenticated),
    db: Session = Depends(get_db),
):
    cart = User.delete_all_cart(requested_user_id, db)
    return count_cart(cart)


@router.get("/cart", status_code=status.HTTP_200_OK, response_model=schemas.CartResp)
def get_cart(
    requested_user_id: int = Depends(is_authenticated), db: Session = Depends(get_db)
):
    cart = User.get_cart(requested_user_id, db)
    return count_cart(cart)


@router.post("/cart/promocode", status_code=status.HTTP_200_OK, response_model=schemas.CartResp)
def add_promocode(
    promocode: str, requested_user_id: int = Depends(is_authenticated), db: Session = Depends(get_db)
):
    promocode_db = Promocode.get_promocode_by_code(promocode, db)
    if not promocode_db:
        raise promocode_not_found_exception
    cart = User.add_cart_promocode(promocode_db.id, requested_user_id, db)

    return count_cart(cart)


@router.delete("/cart/promocode", status_code=status.HTTP_200_OK, response_model=schemas.CartResp)
def delete_promocode(
    requested_user_id: int = Depends(is_authenticated), db: Session = Depends(get_db)
):

    cart = User.delete_cart_promocode(requested_user_id, db)

    return count_cart(cart)


@router.post(
    "/delivery_address",
    status_code=status.HTTP_200_OK,
    response_model=schemas.DeliveryAddress,
)
def add_address(
    address: schemas.DeliveryAddressBase,
    requested_user_id: int = Depends(is_authenticated),
    db: Session = Depends(get_db),
):
    address_db = User.add_address(requested_user_id, address.address, db)
    return address_db


@router.get(
    "/delivery_address",
    status_code=status.HTTP_200_OK,
    response_model=List[schemas.DeliveryAddress],
)
def get_address(
    requested_user_id: int = Depends(is_authenticated),
    db: Session = Depends(get_db),
):
    return db.query(models.DeliveryAddress).filter(
        models.DeliveryAddress.user_id == requested_user_id
    ).all()
