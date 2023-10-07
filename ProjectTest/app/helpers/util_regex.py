"""
regex declarations.
"""
PASSWORD = r"^.{4,64}$"
EMAIL = r"^[a-zA-Z0-9]+(?:\.[a-zA-Z0-9]+)*@[a-zA-Z0-9]+(?:\.[a-zA-Z0-9]+)*$"
PHONE_NUMBER = r"^[0-9 +]{5,30}$"
LOCALE = r"^[\a-zA-Z]{2,8}$"
