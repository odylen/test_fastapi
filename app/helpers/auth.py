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
from app.exceptions.sms import sending_sms_exception
from app.settings import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(password: str, hashed_password: str):
    print(password, hashed_password)
    return pwd_context.verify(password, hashed_password)


def get_password_hash(password: str):
    return pwd_context.hash(password)


def create_access_token(user_id: Dict):
    expire = datetime.utcnow() + timedelta(minutes=settings.access_token_expire_minutes)
    data = {
        "id": user_id,
    }
    to_encode = data.copy()
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, settings.secret_key, algorithm=settings.algorithm
    )
    return encoded_jwt


def generate_code(code_length) -> str:
    code = ''.join(random.choices(string.digits, k=code_length))
    return code


async def send_sms(phone: str, message: str):
    params = {
        "method": "push_msg",
        "email": settings.sms_email,
        "password": settings.sms_password,
        "text": message,
        "phone": phone,
        "sender_name": settings.sms_sender,
        "format": "json",
    }
    async with ClientSession() as session:
        resp = await session.post("http://ssl.bs00.ru/", params=params)
    try:
        err_code = (await resp.json())['response']['msg']['err_code']
        if err_code == 0:
            return True
    except:
        pass
    return False
