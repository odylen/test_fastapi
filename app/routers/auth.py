import os
from datetime import datetime, timedelta

from fastapi import APIRouter, status, Body, Depends
from sqlalchemy.orm import Session

from app import schemas
from app.exceptions.sms import (
    sending_sms_exception,
    code_not_found_exception,
    incorrect_code_exception,
    code_not_confirmed_exception, code_expired_exception,
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
from app.settings import SMS_CODE_LENGTH, SMS_CODE_EXPIRE_MINUTES

router = APIRouter(prefix="/api/auth", tags=["auth"])


async def generate_and_send_sms(phone: str, db: Session) -> int:
    code = generate_code(SMS_CODE_LENGTH)
    print(code)
    resp = await send_sms(phone=phone, message=code)
    expire = datetime.utcnow() + timedelta(
        minutes=SMS_CODE_EXPIRE_MINUTES
    )
    db_code = PhoneCode.create_phone_code(phone=phone, code=code, expire=expire, db=db)

    return db_code.id


@router.post(
    "/send_code", status_code=status.HTTP_200_OK, response_model=schemas.SendTokenResponse
)
async def send_code(phone: str, db: Session = Depends(get_db)):
    code_id = await generate_and_send_sms(phone=phone, db=db)
    print(code_id)
    return schemas.SendTokenResponse(code_id=code_id)


@router.post(
    "/validate_code", status_code=status.HTTP_200_OK, response_model=schemas.SendTokenResponse
)
async def validate_code(
    code_id: int = Body(...), phone_code: str = Body(...), db: Session = Depends(get_db)
):
    db_phone_code = PhoneCode.get_code_by_id(code_id, db)
    if not db_phone_code:
        raise code_not_found_exception
    if db_phone_code.code != phone_code:
        raise incorrect_code_exception
    if datetime.utcnow() > db_phone_code.expire:
        raise code_expired_exception
    PhoneCode.confirm_phone(code_id, db)
    return schemas.ValidateTokenResponse(code_id=code_id, confirmed=True)


@router.post("/login", status_code=status.HTTP_200_OK, response_model=schemas.Token)
def login(
    user: schemas.UserBase,
    code_id=Body(default=None),
    db: Session = Depends(get_db),
):
    db_user = User.get_user_by_phone(user.phone, db)
    if not db_user:
        if code_id:
            phone_code = PhoneCode.get_code_by_id(code_id, db)
            if phone_code.confirmed:
                db_user = User.create_user(
                    schemas.UserBase(phone=phone_code.phone, password=user.password), db
                )
            else:
                raise code_not_confirmed_exception
        else:
            raise user_not_found_exception
    else:
        if not verify_password(user.password, db_user.password):
            raise incorrect_password_exception
    access_token = create_access_token(db_user.id)
    return schemas.Token(access_token=f"Bearer {access_token}")
