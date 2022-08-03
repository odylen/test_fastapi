from datetime import datetime, timedelta

from fastapi import APIRouter, status, Body, Depends
from sqlalchemy.orm import Session

from app.api.auth import schemas
from app.api.auth.queries import PhoneCode
from app.api.common.helpers import generate_code
from app.api.common.queries import User
from app.api.user.schemas import UserBase
from app.database import models
from app.api.auth.exceptions import (
    sending_sms_exception,
    incorrect_code_exception,
    code_expired_exception,
)
from app.api.auth.helpers import (
    create_access_token,
    send_sms,
)

from app.api.common.schemas import RequestStatus
from app.database.db import get_db

from app.settings import settings

router = APIRouter(prefix="/auth", tags=["auth"])


async def generate_and_send_sms(phone: str, db: Session) -> bool:
    code = generate_code(settings.sms_code_length)
    send_status = await send_sms(phone=phone, message=code)
    if not send_status:
        return False
    expire = datetime.utcnow() + timedelta(minutes=settings.sms_code_expire_minutes)
    PhoneCode.create_phone_code(phone=phone, code=code, expire=expire, db=db)
    return True


@router.post(
    "/send_code",
    status_code=status.HTTP_200_OK,
    response_model=RequestStatus
)
async def send_code(phone: str, db: Session = Depends(get_db)):
    send_status = await generate_and_send_sms(phone=phone, db=db)
    if not send_status:
        raise sending_sms_exception
    return RequestStatus()


@router.post("/login", status_code=status.HTTP_200_OK, response_model=schemas.Token)
def login(
    login_scheme: schemas.LoginScheme,
    db: Session = Depends(get_db),
):
    phone = login_scheme.phone
    code = login_scheme.code
    db_phone_code = (
        db.query(models.PhoneCode)
        .filter(models.PhoneCode.phone == phone, models.PhoneCode.code == code)
        .first()
    )

    if not db_phone_code:

        raise incorrect_code_exception
    print(db_phone_code.expire, datetime.utcnow())

    if datetime.utcnow() > db_phone_code.expire:
        db.query(models.PhoneCode).filter(models.PhoneCode.phone == phone, models.PhoneCode.code == code).delete()
        db.commit()
        raise code_expired_exception

    db_user = User.get_user_by_phone(phone, db)
    if not db_user:
        db_user = User.create_user(UserBase(phone=phone), db)
    access_token = create_access_token(db_user.id)

    db.query(models.PhoneCode).filter(models.PhoneCode.phone == phone, models.PhoneCode.code == code).delete()
    db.commit()
    return schemas.Token(access_token=f"Bearer {access_token}")
