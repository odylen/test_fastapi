from pydantic import BaseModel


class Token(BaseModel):
    access_token: str


class SendTokenResponse(BaseModel):
    code_id: str


class ValidateTokenResponse(BaseModel):
    code_id: str
    confirmed: bool


class LoginScheme(BaseModel):
    phone: str
    code: str
