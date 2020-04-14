import re

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


def format_date(date):
    """
    Return a date format for comment item.
    """
    match = re.search(r"(\d+:\d+)", date)
    hour = match.group(1)
    match = re.search(r"(\d+-\d+-\d+)", date)
    day = match.group(1)
    return day + "  " + hour
