from pydantic import BaseSettings


class Settings(BaseSettings):
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

    access_token_expire_minutes: int = 100

    sms_code_expire_minutes: int = 100
    sms_code_length: int = 5

    card_code_length: int = 10

    postgres_db: str
    postgres_user: str
    postgres_password: str
    postgres_host: str

    sms_email: str
    sms_password: str
    sms_sender: str

    algorithm: str
    secret_key: str


settings = Settings()
