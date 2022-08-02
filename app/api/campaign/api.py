from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status

from app.api.campaign import schemas
from app.api.campaign.exceptions import campaign_not_found_exception
from app.api.campaign.queries import Campaign
from app.api.common.schemas import RequestStatus
from app.database import models
from app.database.db import get_db
from app.api.common.exceptions import not_admin_exception
from app.middleware.auth import is_admin

router = APIRouter(prefix="/campaign", tags=["campaign"])


@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    response_model=schemas.Campaign,
)
def get_campaign(
    campaign_id: int,
    db: Session = Depends(get_db),
):
    campaign_db = Campaign.get_campaign_by_id(campaign_id, db)
    if not campaign_db:
        raise campaign_not_found_exception
    return campaign_db


@router.post("/", status_code=status.HTTP_200_OK, response_model=schemas.Campaign)
def add_campaign(
    campaign: schemas.CampaignAdd,
    is_user_admin: bool = Depends(is_admin),
    db: Session = Depends(get_db),
):
    if not is_user_admin:
        raise not_admin_exception
    return Campaign.create_campaign(campaign, db)


@router.put("/", status_code=status.HTTP_200_OK, response_model=schemas.Campaign)
def edit_campaign(
    campaign: schemas.CampaignEdit,
    is_user_admin: bool = Depends(is_admin),
    db: Session = Depends(get_db),
):
    if not is_user_admin:
        raise not_admin_exception
    campaign_db = Campaign.get_campaign_by_id(campaign.id, db)
    if not campaign_db:
        raise campaign_not_found_exception
    return Campaign.edit_campaign(campaign, db)


@router.delete("/", status_code=status.HTTP_200_OK, response_model=RequestStatus)
def delete_campaign(
    campaign_id: int,
    is_user_admin: bool = Depends(is_admin),
    db: Session = Depends(get_db),
):
    if not is_user_admin:
        raise not_admin_exception
    campaign_db = Campaign.get_campaign_by_id(campaign_id, db)
    if not campaign_db:
        raise campaign_not_found_exception
    Campaign.delete_campaign(campaign_id, db)
    return RequestStatus()


@router.get(
    "/all",
    status_code=status.HTTP_200_OK,
    response_model=List[schemas.CampaignBase],
)
def get_all_campaigns(
    db: Session = Depends(get_db),
):
    return db.query(models.Campaign).order_by(models.Campaign.sort).all()
