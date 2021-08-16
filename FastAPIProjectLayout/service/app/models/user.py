"""
user collection ODM.
"""
import datetime
from typing import List, Optional

from odmantic import Field, Model

from app.models.base_dao import BaseDAO
from helpers import util_regex
from helpers.util_enum import BaseEnum


class UserRoleChoices(BaseEnum):
    """Choices for user roles."""
    admin = "admin"
    user = "user"


class User(Model):
    """user model document."""
    id: str = Field(
        primary_field=True,
        regex=util_regex.USER_ID,
        description="username",
    )
    created_datetime: datetime.datetime = Field(
        default_factory=datetime.datetime.utcnow,
    )
    updated_datetime: datetime.datetime = Field(
        default_factory=datetime.datetime.utcnow,
    )
    password: str
    roles: List[UserRoleChoices]
    name: str = Field(regex=util_regex.TEXT)
    email: Optional[str] = Field(regex=util_regex.TEXT)
    disabled: bool = False


class UserDAO(BaseDAO):
    """user document data access object."""
    model = User
