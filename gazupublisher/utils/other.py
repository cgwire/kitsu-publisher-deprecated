import re
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


def extract_date(date):
    """
    Extract day and hour from database date format.
    """
    match = re.search(r"(\d+:\d+)", date)
    hour = match.group(1)
    match = re.search(r"(\d+-\d+-\d+)", date)
    day = match.group(1)
    return day, hour

def format_date(date):
    """
    Return a more pleasant format for date and hour display.
    """
    day, hour = extract_date(date)
    return day + " " + hour

def combine_colors(c1, c2):
    """
    Return the mix color given two colors.
    """
    c3 = QtGui.QColor()
    c3.setRed((c1.red() + c2.red()) / 2)
    c3.setGreen((c1.green() + c2.green()) / 2)
    c3.setBlue((c1.blue() + c2.blue()) / 2)
    return c3
