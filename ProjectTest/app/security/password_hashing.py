"""
Password hashing management.
"""
from passlib.context import CryptContext

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(plain_pwd: str) -> str:
    """Hashes a password.
    :param plain_pwd: plain password
    :type plain_pwd: str
    :return: hashed password
    :rtype: str
    """
    return password_context.hash(plain_pwd)


def verify_password(plain_pwd: str, hashed_pwd: str) -> bool:
    """Verifies password by comparison.
    :param plain_pwd: plain password
    :type plain_pwd: str
    :param hashed_pwd: hashed password
    :type hashed_pwd: str
    :return: True if matched, False otherwise
    :rtype: bool
    """
    return password_context.verify(plain_pwd, hashed_pwd)
