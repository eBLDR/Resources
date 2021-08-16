"""
Security management.
"""
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from app.models.user import UserDAO
from app.security import jwt_token, password_hashing

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


async def get_current_user(token: str = Depends(oauth2_scheme)):
    """Gets current user given an authentication token.
    :param token: user's authentication token
    :type token: str
    :return: current user
    :rtype: UserDAO.model
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    token_data = jwt_token.decode_token(token)

    if not token_data:
        raise credentials_exception

    user = await UserDAO.find_one_by_id(token_data.username)
    if not user:
        raise credentials_exception

    if user.disabled:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user",
        )

    return user


async def authenticate_user(username: str, password: str):
    """Validates user by username and password.
    :param username: username
    :type username: str
    :param password: password
    :type password: str
    :return: True if valid user, False otherwise
    :rtype: [UserDAO.model, bool]
    """
    user = await UserDAO.find_one_by_id(username)
    if not user or user.disabled or not password_hashing.verify_password(
            password,
            user.password,
    ):
        return False

    return user
