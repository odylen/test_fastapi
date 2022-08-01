from sqlalchemy.orm import Session

from app.api.campaign import schemas
from app.database import models


class Campaign:
    @staticmethod
    def get_campaign_by_id(campaign_id: int, db: Session) -> models.Campaign:
        return db.query(models.Campaign).filter(models.Campaign.id == campaign_id).first()

    @staticmethod
    def create_campaign(campaign: schemas.CampaignAdd, db: Session) -> models.Campaign:
        db_campaign = models.Campaign(**campaign.dict())
        db.add(db_campaign)
        db.commit()
        db.refresh(db_campaign)
        return db_campaign

    @staticmethod
    def edit_campaign(campaign: schemas.Campaign, db: Session) -> models.Campaign:
        db_campaign: models.Campaign = db.query(models.Campaign).filter(models.Campaign.id == campaign.id).first()
        for key, value in campaign.dict().items():
            if value:
                setattr(db_campaign, key, value)
        db.add(db_campaign)
        db.commit()
        db.refresh(db_campaign)
        return db_campaign

    @staticmethod
    def delete_campaign(campaign_id: int, db: Session):
        db.query(models.Campaign).filter(models.Campaign.id == campaign_id).delete()
        db.commit()
