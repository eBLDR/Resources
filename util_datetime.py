"""
Util methods for datetime management.
"""
import datetime

DATE_FORMAT = "%Y%m%d"
TIME_FORMAT = "%H%M%S"


def parse_date(value):
    """Convert date-like str to date object.
    :param value: date-like str
    :type value: str
    :return: date object
    :rtype: datetime.date
    """
    return datetime.datetime.strptime(value, DATE_FORMAT).date()


def parse_time(value):
    """Convert time-like str to time object.
    :param value: time-like str
    :type value: str
    :return: time object
    :rtype: datetime.time
    """
    return datetime.datetime.strptime(value, TIME_FORMAT).time()


def combine_date_and_time(date, time):
    """Combines date and time into datetime.
    :param date: date object
    :type date: datetime.date
    :param time: time object
    :type time: datetime.time
    :return: datetime with date and time combined
    :rtype: datetime.datetime
    """
    return datetime.datetime.combine(date, time)


def earliest_datetime_by_date(date):
    """Calculates earliest datetime given a date.
    :param date: date object
    :type date: datetime.date
    :return: earliest date's datetime
    :rtype: datetime.datetime
    """
    return combine_date_and_time(date, datetime.datetime.min.time())


def latest_datetime_by_date(date):
    """Calculates latest datetime given a date.
    :param date: date object
    :type date: datetime.date
    :return: latest date's datetime
    :rtype: datetime.datetime
    """
    return combine_date_and_time(date, datetime.datetime.max.time())
