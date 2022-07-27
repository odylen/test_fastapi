from fastapi import APIRouter, Depends, HTTPException
from fastapi_pagination import Page
from sqlalchemy.orm import Session
from starlette import status

from app import schemas
from app.database import models
from app.database.db import get_db
from app.database.queries import User, BonusCard
from app.exceptions.user import not_admin_exception
from app.middleware.auth import is_autheticated, is_admin
from fastapi_pagination.ext.sqlalchemy import paginate

router = APIRouter(prefix="/bonus_card", tags=["bonus"])


@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    response_model=schemas.BonusCard,
)
def get_bonus_card(
    card_id: int,
    requested_user_id: int = Depends(is_autheticated),
    is_user_admin: bool = Depends(is_admin),
    db: Session = Depends(get_db),
):
    card = BonusCard.get_card_by_id(card_id, db)
    if not card:
        raise HTTPException(status_code=404, detail="Card not found")
    if card.user_id != requested_user_id and not is_user_admin:
        raise not_admin_exception
    return card


@router.post("/", status_code=status.HTTP_200_OK, response_model=schemas.BonusCard)
def add_bonus_card(
    user_id=None,
    requested_user_id: int = Depends(is_autheticated),
    is_user_admin: bool = Depends(is_admin),
    db: Session = Depends(get_db),
):
    if user_id and user_id != requested_user_id and not is_user_admin:
        raise not_admin_exception
    if not user_id:
        user_id = requested_user_id
    return BonusCard.create_bonus_card(user_id, db)


@router.put("/", status_code=status.HTTP_200_OK, response_model=schemas.BonusCard)
def edit_bonus_card(
    card_id: int,
    user_id: int = None,
    card_code: str = None,
    is_user_admin: bool = Depends(is_admin),
    db: Session = Depends(get_db),
):
    if not is_user_admin:
        raise not_admin_exception
    db_card = BonusCard.get_card_by_id(card_id, db)
    if not db_card:
        raise HTTPException(status_code=404, detail="Card not found")
    return BonusCard.edit_bonus_card(card_id, user_id=user_id, code=card_code, db=db)


@router.delete("/", status_code=status.HTTP_200_OK)
def delete_bonus_card(
    card_id,
    is_user_admin: bool = Depends(is_admin),
    db: Session = Depends(get_db),
):
    if not is_user_admin:
        raise not_admin_exception
    db_card = BonusCard.get_card_by_id(card_id, db)
    if not db_card:
        raise HTTPException(status_code=404, detail="Card not found")
    BonusCard.delete_bonus_card(card_id, db)
    return {'success': True}


@router.get(
    "/all",
    status_code=status.HTTP_200_OK,
    response_model=Page[schemas.BonusCard],
)
def get_all_cards(
    user_id: str = None,
    requested_user_id: int = Depends(is_autheticated),
    is_user_admin: bool = Depends(is_admin),
    db: Session = Depends(get_db),
):
    if user_id and user_id != requested_user_id and not is_user_admin:
        raise not_admin_exception
    if not is_user_admin:
        return paginate(
            db.query(models.BonusCard).filter(models.BonusCard.user_id == user_id)
        )

    if user_id:
        return paginate(
            db.query(models.BonusCard).filter(models.BonusCard.user_id == user_id)
        )

    return paginate(db.query(models.BonusCard))
