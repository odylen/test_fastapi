from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from starlette import status

from app.api.campaign.exceptions import (
    order_not_found_exception,
    order_forbidden_exception,
)
from app.api.common.helpers import count_cart
from app.api.common.queries import User
from app.api.order import schemas
from app.api.order.exceptions import (
    invalid_order_input_exception,
    invalid_order_cart_input_exception,
)
from app.api.order.helpers import generate_payment_url
from app.api.user.schemas import CartResp
from app.database import models
from app.database.db import get_db
from app.database.models import OrderType
from app.middleware.auth import is_authenticated

router = APIRouter(prefix="/order", tags=["order"])


@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    response_model=schemas.Order,
)
def get_order_status(
    order_id: int,
    requested_user_id: int = Depends(is_authenticated),
    db: Session = Depends(get_db),
):
    order = db.query(models.Order).filter(models.Order.id == order_id).first()
    if not order:
        raise order_not_found_exception
    if order.user_id != requested_user_id:
        raise order_forbidden_exception
    return order


@router.post("/", status_code=status.HTTP_200_OK, response_model=schemas.Order)
def create_order(
    order: schemas.OrderCreate,
    requested_user_id: int = Depends(is_authenticated),
    db: Session = Depends(get_db),
):
    if (order.type == OrderType.PICKUP and not order.bakery_id) or (
        order.type == OrderType.DELIVERY and not order.delivery_address_id
    ):
        raise invalid_order_input_exception
    db_user = User.get_user_by_id(requested_user_id, db)
    cart = count_cart(db_user.cart)
    if cart.total <= 0:
        raise invalid_order_cart_input_exception
    payment_url = generate_payment_url()
    order = models.Order(**order.dict())
    order.payment_link = payment_url
    order.total = cart.total
    order.user_id = requested_user_id
    order.cart = CartResp.from_orm(cart).dict()
    db.add(order)
    User.delete_all_cart(requested_user_id, db)
    if db_user.cart.promocode:
        promo = db_user.cart.promocode
        User.delete_cart_promocode(requested_user_id, db)
        db.delete(promo)

    db.commit()

    db.refresh(order)
    return order


@router.get(
    "/status",
    status_code=status.HTTP_200_OK,
    response_model=schemas.OrderStatus,
)
def get_order_status(
    order_id: int,
    requested_user_id: int = Depends(is_authenticated),
    db: Session = Depends(get_db),
):
    order = db.query(models.Order).filter(models.Order.id == order_id).first()
    if not order:
        raise order_not_found_exception
    if order.user_id != requested_user_id:
        raise order_forbidden_exception
    return order


@router.get(
    "/all",
    status_code=status.HTTP_200_OK,
    response_model=List[schemas.Order],
)
def get_orders(
    requested_user_id: int = Depends(is_authenticated),
    db: Session = Depends(get_db),
):
    return (
        db.query(models.Order).filter(models.Order.user_id == requested_user_id).all()
    )
