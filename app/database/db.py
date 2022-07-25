from os import environ

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = f'postgresql://{environ.get("POSTGRES_USER")}:{environ.get("POSTGRES_PASSWORD")}@{environ.get("POSTGRES_HOST")}:5432/{environ.get("POSTGRES_DB")}'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

DBSession = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Dependency
def get_db():
    db = DBSession()
    try:
        yield db
    finally:
        db.close()
