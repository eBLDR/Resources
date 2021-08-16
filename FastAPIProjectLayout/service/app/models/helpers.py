"""
embedded helpers ODM.
"""
from typing import List, Optional

from odmantic import EmbeddedModel, Field

from helpers import util_regex


class Name(EmbeddedModel):
    """name embedded model document."""
    first_name: str = Field(regex=util_regex.TEXT)
    surname_1: str = Field(regex=util_regex.TEXT)
    surname_2: Optional[str] = Field(regex=util_regex.TEXT)


class Address(EmbeddedModel):
    """address embedded model document."""
    street: Optional[str] = Field(regex=util_regex.TEXT)
    number: Optional[str] = Field(regex=util_regex.TEXT)
    municipality: Optional[str] = Field(regex=util_regex.TEXT)
    region: Optional[str] = Field(regex=util_regex.TEXT)
    province: Optional[str] = Field(regex=util_regex.TEXT)
    postal_code: Optional[str] = Field(regex=util_regex.TEXT)
    country: Optional[str] = Field(regex=util_regex.TEXT)


class ContactDetails(EmbeddedModel):
    """contact_details embedded model document."""
    name: Name
    birthdate: Optional[str] = Field(regex=util_regex.DATE)
    phone: Optional[List[str]] = Field(regex=util_regex.PHONE_NUMBER)
    email: Optional[str] = Field(regex=util_regex.TEXT)
    address: Optional[Address]
    locale: Optional[str] = Field(regex=util_regex.LOCALE)
