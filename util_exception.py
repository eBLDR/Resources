"""
Util methods for exception management.
"""


class BaseCustomException(Exception):
    """Base custom exception."""

    def __init__(self, msg):
        self.msg = msg
        super().__init__()
