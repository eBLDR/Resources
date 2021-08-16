"""
regex declarations.
"""
WORD_CODE = r"^[\w-]{4,32}$"
PASSWORD = r"^.{5,32}$"
TEXT = r"^[\\p{L}\w \/\\.,;:'\"()#@-]{1,128}$"
PHONE_NUMBER = r"^[0-9 +]{5,30}$"
LOCALE = r"^[\w-]{2,8}$"
DATE = r"^\d{4}-(0[1-9]|1[0-2])-(0[1-9]|[12][0-9]|3[01])$"
