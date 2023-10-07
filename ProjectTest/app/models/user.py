"""
User collection ORM.
"""
import datetime
from typing import Optional

from sqlmodel import Field, select

from app.helpers import util_regex
from app.models.base_model import BaseModel


class User(BaseModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    active: bool = Field(default=True, nullable=False)
    created_ts: datetime.datetime = Field(default_factory=datetime.datetime.utcnow)
    updated_ts: datetime.datetime = Field(default_factory=datetime.datetime.utcnow)
    username: str = Field(max_length=64, unique=True, nullable=False)
    password: str = Field(max_length=64, unique=False, nullable=False, regex=util_regex.PASSWORD)
    locale: str = Field(max_length=8, unique=False, default="EN", regex=util_regex.LOCALE)
    email: str = Field(max_length=128, unique=False, nullable=False, regex=util_regex.EMAIL)
    phone: Optional[str] = Field(max_length=32, unique=False, nullable=True, regex=util_regex.PHONE_NUMBER)

    @classmethod
    async def find_one_by_username(cls, username: str):
        """Read one user by username."""
        statement = select(cls).where(cls.username == username)
        return await cls.find_one(statement)
