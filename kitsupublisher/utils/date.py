"""
The dates in the database are written with this format : "1900-01-01T00:00:00".
This module contains functions to manage the display of these dates and other
utility functions.
"""

import datetime
import pytz


def compare_date(d1, d2):
    """
    Return whether d1 is more recent than d2
    """
    date1 = extract_date(d1)
    date2 = extract_date(d2)
    return date1 > date2


def current_date():
    return datetime.date.today()


def is_date_x_days_old(date, x):
    """
    Given a period of x days, return if the given date is within the last x days
    from now.
    """
    today_date = current_date()
    x_days = datetime.timedelta(days=x)
    limit_date = today_date - x_days
    return date > limit_date


def extract_date(date):
    """
    Extract day and hour from database date format.
    """
    return datetime.datetime.strptime(date, "%Y-%m-%dT%H:%M:%S")


def from_datetime_to_date(datetime_object):
    """
    Convert a datetime object into a date object
    """
    return datetime.datetime.date(datetime_object)


def format_comment_date(user, comment_date):
    """
    Return a more pleasant format for comment date display.
    """
    date = extract_date(comment_date)
    date = utc_to_local(user, date)
    return date.strftime("%Y-%m-%d | %H:%M:%S")


def format_table_date(user, table_date):
    """
    Return a more pleasant format for date display.
    """
    date = extract_date(table_date)
    date = utc_to_local(user, date)
    return date.strftime("%Y-%m-%d")


def from_min_to_day(time, organisation=None):
    """
    Convert a str time with minutes as a unit (i.e. a task duration), into
    another str rounded time with an 8-hour day as a unit.
    If an organisation is given as parameter, we use its field `hours_by_day`
    to know how long a working day lasts.
    """
    if organisation is not None:
        hours_per_day = organisation["hours_by_day"] or 8
    else:
        hours_per_day = 8
    day_estimation = int(time) / 60 / hours_per_day
    return str(round(day_estimation, 1))


def utc_to_local(user, utc_dt):
    """
    Turn a date into a date matching use timezone. It's useful when you need
    to display a date.
    """
    local_tz = pytz.timezone(user["timezone"])
    local_dt = utc_dt.replace(tzinfo=pytz.utc).astimezone(local_tz)
    return local_tz.normalize(local_dt)
