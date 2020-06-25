import re

import Qt.QtWidgets as QtWidgets
import Qt.QtGui as QtGui
import Qt.QtCore as QtCore


class AnimatedLabel(QtWidgets.QLabel):
    """
    QLabel with animated background color.
    Used to display errors.
    """

    def __init__(self):
        super(AnimatedLabel, self).__init__()
        self.setStyleSheet(
            """
            background-color: #CC4444;
            color: #F5F5F5;
            padding: 5px;
            """
        )
        self.setWordWrap(True)
        self.create_animation()

    def create_animation(self):
        """
        Create the animation of the color background.
        """
        color_begin = QtGui.QColor("#943434")
        color_end = QtGui.QColor("#CC4444")
        self.color_anim = QtCore.QPropertyAnimation(self, b"background_color")
        self.color_anim.setStartValue(color_begin)
        self.color_anim.setEndValue(color_end)
        self.color_anim.setDuration(400)

    def start_animation(self):
        """
        Start the animation of the color background.
        """
        self.color_anim.stop()
        self.color_anim.start()

    def get_back_color(self):
        """
        Get the background color.
        """
        return self.palette().color(QtGui.QPalette.Window)

    def set_back_color(self, color):
        """
        Set the given color as background color by parsing the style sheet.
        """
        style = self.styleSheet()
        pattern = "background-color:[^\n;]*"
        new = "background-color: %s" % color.name()
        style = re.sub(pattern, new, style, flags=re.MULTILINE)
        self.setStyleSheet(style)

    # Property to animate : the label background color
    background_color = QtCore.Property(
        QtGui.QColor, get_back_color, set_back_color
    )

