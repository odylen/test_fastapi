from fastapi import Header, Depends
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from app.api.common.queries import User
from app.database.db import get_db
import os

from app.database.models import AccountType
from app.api.common.exceptions import token_exception


async def is_authenticated(authorization: str = Header(...)):
    token: str = authorization.split()[-1]
    try:
        payload = jwt.decode(
            token, os.environ.get("SECRET_KEY"), algorithms=os.environ.get("ALGORITHM")
        )
        if payload.get("type") != 'access':
            raise token_exception
        return payload.get("id")
    except JWTError as e:
        raise token_exception


async def is_admin(authorization: str = Header(...), db: Session = Depends(get_db)):
    token: str = authorization.split()[-1]
    try:
        payload = jwt.decode(
            token, os.environ.get("SECRET_KEY"), algorithms=os.environ.get("ALGORITHM")
        )
        user_id = payload.get("id")
    except JWTError:
        raise token_exception
    return User.get_user_by_id(user_id, db).type == AccountType.ADMIN
