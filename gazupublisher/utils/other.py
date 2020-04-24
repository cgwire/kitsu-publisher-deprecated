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


def combine_colors(c1, c2, factor=0.5):
    """
    Return the mix color given two colors.
    """
    c3 = QtGui.QColor()
    c3.setRed(int((factor * c1.red() + (1 - factor) * c2.red())))
    c3.setGreen(int((factor * c1.green() + (1 - factor) * c2.green())))
    c3.setBlue(int((factor * c1.blue() + (1 - factor) * c2.blue())))
    return c3
