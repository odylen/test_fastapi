import os
from datetime import datetime, timedelta

from fastapi import APIRouter, status, Body, Depends
from sqlalchemy.orm import Session

from app import schemas
from app.database import models
from app.exceptions.sms import (
    sending_sms_exception,
    code_not_found_exception,
    incorrect_code_exception,
    code_not_confirmed_exception,
    code_expired_exception,
)
from app.helpers.auth import (
    create_access_token,
    verify_password,
    generate_code,
    send_sms,
)

from app.database.queries import User, PhoneCode
from app.database.db import get_db
from app.middleware.auth import is_autheticated

from app.exceptions.user import user_not_found_exception, incorrect_password_exception
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
    response_model=schemas.SendTokenResponse,
)
async def send_code(phone: str, db: Session = Depends(get_db)):
    send_status = await generate_and_send_sms(phone=phone, db=db)
    if not send_status:
        raise sending_sms_exception
    return {"success": True}


@router.post("/login", status_code=status.HTTP_200_OK, response_model=schemas.Token)
def login(
    phone: str = Body(...),
    code: str = Body(...),
    db: Session = Depends(get_db),
):
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
        db_user = User.create_user(schemas.UserBase(phone=phone), db)
    access_token = create_access_token(db_user.id)

    db.query(models.PhoneCode).filter(models.PhoneCode.phone == phone, models.PhoneCode.code == code).delete()
    db.commit()
    return schemas.Token(access_token=f"Bearer {access_token}")
