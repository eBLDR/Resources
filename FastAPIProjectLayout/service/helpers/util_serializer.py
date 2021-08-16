"""
Util methods for JSON serializing management.
"""
import datetime
from typing import Any


def fallback_default_serializer(value: Any):
    """Fallback default serializer for object-JSON conversion and vice versa.
    :param value: value to serialize
    :type value: Any
    :return: serialized value
    :rtype: str() supported value
    """
    if isinstance(value, (datetime.datetime, datetime.date, datetime.time)):
        return value.isoformat()
