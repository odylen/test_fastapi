import random
import os
import string

from passlib.context import CryptContext
from datetime import datetime, timedelta
from typing import Optional, Dict

from fastapi import status, HTTPException, Header
from sqlalchemy.orm import Session
from jose import JWTError, jwt
from aiohttp import ClientSession

from app.database import models
from app.settings import ACCESS_TOKEN_EXPIRE_MINUTES

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(password: str, hashed_password: str):
    print(password, hashed_password)
    return pwd_context.verify(password, hashed_password)


def get_password_hash(password: str):
    return pwd_context.hash(password)


def create_access_token(user_id: Dict):
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    data = {
        "id": user_id,
    }
    to_encode = data.copy()
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, os.environ.get("SECRET_KEY"), algorithm=os.environ.get("ALGORITHM")
    )
    return encoded_jwt


def generate_code(code_length) -> str:
    code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=code_length))
    return code


async def send_sms(phone: str, message: str):
    params = {
        "method": "push_msg",
        "email": os.environ.get("SMS_EMAIL"),
        "password": os.environ.get("SMS_PASSWORD"),
        "text": message,
        "phone": phone,
        "sender_name": os.environ.get("SMS_SENDER"),
        "format": "json",
    }
    async with ClientSession() as session:
        resp = await session.post("http://ssl.bs00.ru/", params=params)
    return "hjj"
