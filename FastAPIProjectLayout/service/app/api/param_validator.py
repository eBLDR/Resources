"""
Methods for API parameters validations.
"""
from fastapi import HTTPException, status

from helpers import util_datetime
from helpers.util_enum import BaseEnum


class FileFormats(BaseEnum):
    """Formats for file download."""
    csv = "csv"
    json = "json"


def validate_file_format(file_format: str):
    """Validates file format.
    :param file_format: file format
    :type file_format: str
    :return: file format
    :rtype: str
    """
    if not file_format:
        file_format = FileFormats.json

    if file_format not in FileFormats.get_all_values():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Unsupported file format: {file_format}",
        )

    return file_format


def convert_date_param(date_string: str):
    """Validates and convert date-like str to date object.
    :param date_string: date-like str
    :type date_string: str
    :return: date object
    :rtype: datetime.date
    """
    try:
        return util_datetime.parse_date(date_string)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Wrong date format. Standard format is: {util_datetime.DATE_FORMAT}",
        )
