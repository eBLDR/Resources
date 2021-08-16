"""
Routes for user management.
"""
from typing import List

from fastapi import APIRouter

from app.api import crud_handler
from app.models.user import UserDAO
from app.schemas.user import UserGetSchema, UserPatchSchema, UserPostSchema

api_router = APIRouter(
    prefix="/user",
    tags=["user"],
)

resource_dao = UserDAO
post_schema = UserPostSchema
get_schema = UserGetSchema
patch_schema = UserPatchSchema


@api_router.post("", response_model=get_schema)
async def create_user(user_post_schema: post_schema):
    """Create new user document.
    :param user_post_schema: user schema
    :type user_post_schema: post_schema
    :return: user schema
    :rtype: get_schema
    """
    return await crud_handler.create(
        user_post_schema,
        get_schema,
        resource_dao,
    )


@api_router.get("", response_model=List[get_schema])
async def read_all_users():
    """Read user documents.
    :return: user schema
    :rtype: list[get_schema]
    """
    return await get_schema.from_document_array(
        await crud_handler.read_all_documents(resource_dao),
    )


@api_router.get("/{user_id}", response_model=get_schema)
async def read_user(user_id: str):
    """Read user document by id.
    :param user_id: user id
    :type user_id: str
    :return: user schema
    :rtype: get_schema
    """
    return await get_schema.from_document(
        await crud_handler.read_one_document_by_id(resource_dao, user_id),
    )


@api_router.patch("/{user_id}", response_model=get_schema)
async def update_user(user_id: str, user_patch_schema: patch_schema):
    """Update user document.
    :param user_id: user id
    :type user_id: str
    :param user_patch_schema: user schema
    :type user_patch_schema: patch_schema
    :return: user schema
    :rtype: get_schema
    """
    return await crud_handler.update(
        user_id,
        user_patch_schema,
        get_schema,
        resource_dao,
    )
