"""
Security management.
"""
from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from app.models.user import User
from app.security import jwt_token, password_hashing

oauth2 = OAuth2PasswordBearer(tokenUrl="token")

credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Invalid credentials",
    headers={"WWW-Authenticate": "Bearer"},
)


async def get_current_user(token: Annotated[str, Depends(oauth2)]):
    """Gets current user given an authentication token.
    :param token: user's authentication token
    :type token: str
    :return: currently logged user
    :rtype: User
    """
    token_data = jwt_token.decode_token(token)

    if not token_data:
        raise credentials_exception

    user = await User.find_one_by_username(username=token_data.username)
    if not user or not user.active:
        raise credentials_exception

    return user


async def authenticate_user(username: str, password: str):
    """Validates user by username and password.
    :param username: user's username
    :type username: str
    :param password: user's password
    :type password: str
    :return: True if valid user, False otherwise
    :rtype: [User, bool]
    """
    user = await User.find_one_by_username(username)
    if not user or not user.active or not password_hashing.verify_password(
            password,
            user.password,
    ):
        return False

    return user
