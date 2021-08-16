"""
API schemas for user management.
"""
import datetime
from typing import List, Optional

from pydantic import Field

from app.models.user import UserRoleChoices
from app.schemas.base import BaseSchema
from helpers import util_regex


class UserBaseSchema(BaseSchema):
    """User base schema."""
    roles: List[UserRoleChoices]
    name: str = Field(regex=util_regex.TEXT)
    email: Optional[str] = Field(regex=util_regex.TEXT)


class UserPostSchema(UserBaseSchema):
    """Schema for creating (POST) user."""
    id: str = Field(regex=util_regex.USER_ID, description="username")
    password: str = Field(regex=util_regex.PASSWORD)


class UserGetSchema(UserBaseSchema):
    """Schema for reading (GET) user."""
    id: str = Field(regex=util_regex.USER_ID, description="username")
    created_datetime: datetime.datetime
    updated_datetime: datetime.datetime
    disabled: bool


class UserPatchSchema(UserBaseSchema):
    """Schema for updating (PATCH) user."""
    password: Optional[str] = Field(regex=util_regex.PASSWORD)
    roles: Optional[List[UserRoleChoices]]
    name: Optional[str] = Field(regex=util_regex.TEXT)
    disabled: Optional[bool]
