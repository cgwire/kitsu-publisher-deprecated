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
