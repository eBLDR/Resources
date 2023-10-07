"""
Routes for user management.
"""
from typing import Annotated, List

from fastapi import APIRouter, Depends

from app.api import crud_handler
from app.models.user import User
from app.security.security import get_current_user

api_router = APIRouter(
    prefix="/user",
    tags=["user"],
)

resource_dao = User
post_model = User
get_schema = User
patch_schema = User


@api_router.get("/me", response_model=User, response_model_exclude={"password"})
async def read_user_me(current_user: Annotated[User, Depends(get_current_user)]):
    """Read current user.
    :param current_user: currently logged user
    :return: currently logged user
    :rtype: User
    """
    return current_user


@api_router.post("", response_model=User, response_model_exclude={"password"})
async def create_user(user: User):
    """Create new user.
    :param user: new user's data
    :type user: User
    :return: created user
    :rtype: User
    """
    return await crud_handler.create(user)


@api_router.get("", response_model=List[User], response_model_exclude={"password"})
async def read_all_users():
    """Read all users.
    :return: all users
    :rtype: list[User]
    """
    return await crud_handler.read_all(User)


@api_router.get("/{user_id}", response_model=User, response_model_exclude={"password"})
async def read_user(user_id: int):
    """Read user by id.
    :param user_id: user id
    :type user_id: int
    :return: found user
    :rtype: User
    """
    return await crud_handler.read_one_by_id(User, user_id)


@api_router.patch("/{user_id}", response_model=User, response_model_exclude={"password"})
async def update_user(user_id: int, new_user_data: User):
    """Update user.
    :param user_id: user id
    :type user_id: int
    :param new_user_data: new data for existing user
    :type new_user_data: User
    :return: updated user
    :rtype: User
    """
    return await crud_handler.update_by_id(user_id, new_user_data)


@api_router.delete("/{user_id}")
async def delete_user(user_id: int):
    """Delete user.
    :param user_id: user id
    :type user_id: int
    :return: updated user
    :rtype: User
    """
    return await crud_handler.delete(User, user_id)
