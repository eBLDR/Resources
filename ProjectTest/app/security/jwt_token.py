"""
Json Web Token management.
"""
import datetime

from jose import JWTError, jwt
from pydantic import BaseModel

from app.core.config import settings

ALGORITHM = "HS256"


class Token(BaseModel):
    """JWT standard."""
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    """Token data for encoding/decoding."""
    username: str | None = None


def create_access_token(subject: str) -> Token:
    """Generates encoded JWT token.
    :param subject: subject line
    :type subject: str
    :return: token
    :rtype: Token
    """
    data = {
        "sub": subject,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(
            minutes=settings.ACCESS_TOKEN_LIFETIME_MINUTES,
        ),
    }
    return Token(
        access_token=jwt.encode(data, settings.SECRET_KEY, algorithm=ALGORITHM),
    )


def decode_token(token: str):
    """Decodes JWT token.
    :param token: encoded token
    :type token: str
    :return: decoded token data
    :rtype: TokenData
    """
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        return TokenData(username=username) if username is not None else False

    except JWTError:
        return False
