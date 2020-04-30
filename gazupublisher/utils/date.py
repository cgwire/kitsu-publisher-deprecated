"""
The dates in the database are written with this format : "1900-01-01T00:00:00".
This module contains functions to manage the display of these dates and other
utility functions.
"""

import datetime


def compare_date(d1, d2):
    """
    Return whether d1 is more recent than d2
    """
    date1 = extract_date(d1)
    date2 = extract_date(d2)
    return date1 > date2


def extract_date(date):
    """
    Extract day and hour from database date format.
    """
    return datetime.datetime.strptime(date, '%Y-%m-%dT%H:%M:%S')


def format_comment_date(comment_date):
    """
    Return a more pleasant format for comment date display.
    """
    date = extract_date(comment_date)
    return date.strftime('%Y-%m-%d | %H:%M:%S')


def format_table_date(table_date):
    """
    Return a more pleasant format for date and hour display.
    """
    date = extract_date(table_date)
    return date.strftime('%Y-%m-%d')
