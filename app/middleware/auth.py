from fastapi import HTTPException, status, Header, Depends
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from app.database.db import get_db
import os

from app.database.models import AccountType
from app.database.queries import User
from app.exceptions.user import token_exception, not_admin_exception


async def is_autheticated(authorization: str = Header(...), db: Session = Depends(get_db)):
    token: str = authorization.split()[-1]
    try:
        payload = jwt.decode(
            token,
            os.environ.get("SECRET_KEY"),
            algorithms=os.environ.get("ALGORITHM")
        )
        return payload.get("id")
    except JWTError as e:
        print(e)
        raise token_exception


async def is_admin(authorization: str = Header(...), db: Session = Depends(get_db)):
    token: str = authorization.split()[-1]
    try:
        payload = jwt.decode(
            token,
            os.environ.get("SECRET_KEY"),
            algorithms=os.environ.get("ALGORITHM")
        )
        user_id = payload.get("id")
    except JWTError:
        raise token_exception
    return User.get_user_by_id(user_id, db).type == AccountType.ADMIN
