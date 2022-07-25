from typing import List, Union

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status

from app import schemas
from app.database import models
from app.database.db import get_db
from app.database.queries import Campaign
from app.exceptions.user import not_admin_exception
from app.middleware.auth import is_admin

router = APIRouter(prefix="/api", tags=["bonus"])


@router.get(
    "/campaign",
    status_code=status.HTTP_200_OK,
    response_model=schemas.Campaign,
)
def get_campaign(
    campaign_id: int,
    db: Session = Depends(get_db),
):
    campaign_db = Campaign.get_campaign_by_id(campaign_id, db)
    if not campaign_db:
        raise HTTPException(status_code=404, detail="Campaign not found")
    return campaign_db


@router.post("/campaign", status_code=status.HTTP_200_OK, response_model=schemas.Campaign)
def add_campaign(
    campaign: schemas.CampaignAdd,
    is_user_admin: bool = Depends(is_admin),
    db: Session = Depends(get_db),
):
    if not is_user_admin:
        raise not_admin_exception
    return Campaign.create_campaign(campaign, db)


@router.put("/campaign", status_code=status.HTTP_200_OK, response_model=schemas.Campaign)
def edit_campaign(
    campaign: schemas.Campaign,
    is_user_admin: bool = Depends(is_admin),
    db: Session = Depends(get_db),
):
    if not is_user_admin:
        raise not_admin_exception
    return Campaign.edit_campaign(campaign, db)


@router.delete("/campaign", status_code=status.HTTP_200_OK)
def delete_campaign(
    campaign_id,
    is_user_admin: bool = Depends(is_admin),
    db: Session = Depends(get_db),
):
    if not is_user_admin:
        raise not_admin_exception
    Campaign.delete_campaign(campaign_id, db)


@router.get(
    "/campaign/all",
    status_code=status.HTTP_200_OK,
    response_model=List[schemas.CampaignBase],
)
def get_all_cards(
    db: Session = Depends(get_db),
):
    return db.query(models.Campaign).order_by(models.Campaign.sort).all()
