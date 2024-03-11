import os
from typing import Optional

from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.orm import sessionmaker, declarative_base

from app import models
from dotenv import load_dotenv

# Load environment variables from .env file
if os.getenv("ENVIRONMENT") == "docker":
    load_dotenv(os.path.join("..", ".env"))
else:
    load_dotenv(os.path.join("..", ".env.testing"))

SQLALCHEMY_DATABASE_URL = os.environ.get("SQLALCHEMY_DATABASE_URL")

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
models.Base.metadata.create_all(bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_user_by_username(username: str, db: Session) -> Optional[models.User]:
    return db.query(models.User).filter(models.User.username == username).first()


def create_user(username: str, password_hash: str, db: Session) -> models.User:
    user = models.User(username=username, password_hash=password_hash)
    db.add(user)
    db.commit()
    return user
