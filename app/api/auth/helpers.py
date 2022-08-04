import re

from passlib.context import CryptContext
from datetime import datetime, timedelta
from typing import Dict

from jose import jwt
from aiohttp import ClientSession

from app.settings import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def normalize_phone(phone: str):
    phone = "".join(re.findall("\d+", phone))
    if phone.startswith("7"):
        phone = "8" + phone[1:]
    return phone


def create_access_token(user_id: Dict):
    expire = datetime.utcnow() + timedelta(minutes=settings.access_token_expire_minutes)
    data = {
        "id": user_id,
        "type": "access"
    }
    to_encode = data.copy()
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, settings.secret_key, algorithm=settings.algorithm
    )
    return encoded_jwt


def create_refresh_token(user_id: Dict):
    expire = datetime.utcnow() + timedelta(minutes=settings.refresh_token_expire_minutes)
    data = {
        "id": user_id,
        "type": "refresh"
    }
    to_encode = data.copy()
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, settings.secret_key, algorithm=settings.algorithm
    )
    return encoded_jwt


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
        err_code = (await resp.json(content_type=None))["response"]["msg"]["err_code"]
        if err_code == "0":
            return True
    except:
        pass
    return False
