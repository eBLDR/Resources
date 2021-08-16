"""
Password hashing management.
"""
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(plain_password: str):
    """Hashes a password.
    :param plain_password: plain password
    :type plain_password: str
    :return: hashed password
    :rtype: str
    """
    return pwd_context.hash(plain_password)


def verify_password(plain_password, hashed_password):
    """Verifies password by comparison.
    :param plain_password: plain password
    :type plain_password: str
    :param hashed_password: hashed password
    :type hashed_password: str
    :return: True if match, False otherwise
    :rtype: bool
    """
    return pwd_context.verify(plain_password, hashed_password)
