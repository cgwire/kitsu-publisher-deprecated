import re
import datetime

import Qt.QtGui as QtGui

formats = {
    "image": ["png", "jpg", "jpeg"],
    "video": ["mp4", "mov", "wmv"],
    "3D": ["obj"],
}


def is_video(preview_file):
    """
    Return if the given preview file is a video
    """
    ext = preview_file["extension"]
    return ext in formats["video"]


def compare_date(d1, d2):
    """
    Return whether d1 is more recent than d2
    """
    year1, month1, day1, hour1, minute1, second1 = extract_date(d1)
    year2, month2, day2, hour2, minute2, second2 = extract_date(d2)
    date1 = datetime.datetime(int(year1), int(month1), int(day1))
    date2 = datetime.datetime(int(year2), int(month2), int(day2))
    if date1 != date2:
        return date1 > date2
    daytime_second1 = 3600 * hour1 + 60 * minute1 + second1
    daytime_second2 = 3600 * hour2 + 60 * minute2 + second2
    return daytime_second1 > daytime_second2


def extract_date(date):
    """
    Extract day and hour from database date format.
    """
    match = re.match(r"(\d+)-(\d+)-(\d+)T(\d+):(\d+):(\d+)", date)
    return match.groups()


def format_date(date):
    """
    Return a more pleasant format for date display.
    """
    year, month, day, _, _, _ = extract_date(date)
    full_day = year + "-" + month + "-" + day
    return full_day


def format_date_and_hour(date):
    """
    Return a more pleasant format for date and hour display.
    """
    year, month, day, hour, minute, _ = extract_date(date)
    full_day = year + "-" + month + "-" + day
    time = hour + ":" + minute
    return full_day + "  " + time


def combine_colors(c1, c2, factor=0.5):
    """
    Return the mix color given two colors.
    """
    c3 = QtGui.QColor()
    c3.setRed(int((factor * c1.red() + (1 - factor) * c2.red())))
    c3.setGreen(int((factor * c1.green() + (1 - factor) * c2.green())))
    c3.setBlue(int((factor * c1.blue() + (1 - factor) * c2.blue())))
    return c3
