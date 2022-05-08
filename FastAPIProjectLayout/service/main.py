"""
APP instance creation.
Module to be run by uvicorn on app runtime.
"""
import logging

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from app import create_app
from app.core.config import settings
from app.database.engine import close_connection, open_connection
from app.security.jwt_token import Token, create_access_token
from app.security.security import authenticate_user

logging.basicConfig(
    filename=settings.LOGS_FILENAME,
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s: [%(filename)s] %(name)s: %(message)s",
)

app = create_app()


@app.on_event("startup")
def startup_event():
    """App start up handling."""
    logging.info("Application start up.")
    open_connection()


@app.on_event("shutdown")
def shutdown_event():
    """App shut down handling."""
    logging.info("Application shutdown.")
    close_connection()


@app.post("/token", response_model=Token)
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
