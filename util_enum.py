"""
Util methods for enum management.
"""
from enum import Enum


class BaseEnum(str, Enum):
    """Base custom Enum class."""

    @classmethod
    def get_all_values(cls):
        """Generate a list of all the declared values.
        :return: list of values
        :rtype: list
        """
        return [v for v in cls]
