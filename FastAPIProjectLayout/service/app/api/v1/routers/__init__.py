"""
API router initialisation.
"""
from fastapi import APIRouter
from fastapi import Depends, HTTPException, status
from fastapi.responses import PlainTextResponse
from fastapi.security import OAuth2PasswordRequestForm

from app.api.v1.routers import (
    user,
)
from app.core.config import settings
from app.security.jwt_token import Token, create_access_token
from app.security.security import authenticate_user
from app.security.security import get_current_user

api_router = APIRouter(
    prefix=settings.API_V1_STR,
)

routers = [
    user.api_router,
]

for router in routers:
    api_router.include_router(
        router,
        dependencies=[Depends(get_current_user)],
    )


@api_router.get("/ping")
async def ping():
    """Ping service.
    :return: pong
    :rtype: str
    """
    return PlainTextResponse(
        content="pong",
    )


@api_router.post("/token", response_model=Token)
async def token(form_data: OAuth2PasswordRequestForm = Depends()):
    """Token generator from OAuth2 form data.
    :param form_data: OAuth2 form data
    :type form_data: OAuth2PasswordRequestForm
    :return: access token data
    :rtype: dict
    """
    user_ = await authenticate_user(form_data.username, form_data.password)
    if not user_:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return create_access_token(user_.id).dict()
