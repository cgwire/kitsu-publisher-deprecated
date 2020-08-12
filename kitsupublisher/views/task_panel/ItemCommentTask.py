import os

from Qt import QtCore, QtGui, QtWidgets

from kitsupublisher.utils.connection import get_file_data_from_url
from kitsupublisher.utils.colors import combine_colors
from kitsupublisher.utils.date import format_comment_date
from kitsupublisher.utils.file import load_ui_file, get_icon_file
from kitsupublisher.utils.data import get_current_user
from kitsupublisher.ui_data.color import main_color


class WidgetCommentTask(QtWidgets.QWidget):
    """
    A widget to display a comment in the list of comments history.
    """

    def __init__(self, comment):
        super(WidgetCommentTask, self).__init__()
        self.comment = comment
        self.color = self.comment["task_status"]["color"]
        self.setStyleSheet("::section{background-color: %s;}" % main_color)
        self.setup_ui()

    def setup_ui(self):
        load_ui_file("CommentWidget.ui", self)
        self.setLayout(self.gridLayout)

        self.comment_textedit = self.findChild(
            QtWidgets.QTextEdit, "comment_textedit"
        )
        self.profile_picture_label = self.findChild(
            QtWidgets.QLabel, "profile_picture_label"
        )
        self.task_status = self.findChild(QtWidgets.QLabel, "task_status")
        self.date = self.findChild(QtWidgets.QLabel, "date")
        self.sender_name = self.findChild(QtWidgets.QLabel, "sender_name")
        self.option = self.findChild(QtWidgets.QPushButton, "option")
        self.color_header = self.findChild(
            QtWidgets.QPushButton, "color_header"
        )
        self.color_header.setProperty("color_header", True)
        self.color_header_top = self.findChild(
            QtWidgets.QPushButton, "color_header_2"
        )
        self.color_header_top.setProperty("color_header", True)
        self.color_header_bottom = self.findChild(
            QtWidgets.QPushButton, "color_header_3"
        )
        self.color_header_bottom.setProperty("color_header", True)

        self.display_profile_picture()
        self.display_task_status()
        self.display_sender_name()
        self.display_creation_date()
        self.display_comment()
        self.hide_button()
        self.header()

    def display_sender_name(self):
        """
        Display the name of the comment author.
        """
        name = (
            self.comment["person"]["first_name"]
            + " "
            + self.comment["person"]["last_name"]
        )
        self.sender_name.setStyleSheet("font-weight: bold;font: 12pt")
        self.sender_name.setText(name)

    def display_creation_date(self):
        """
        Display the creation date of the comment.
        """
        user = get_current_user()
        creation_date = format_comment_date(user, self.comment["created_at"])
        self.date.setStyleSheet("font: 12pt")
        self.date.setText(creation_date)

    def display_comment(self):
        """
        Display the comment.
        """
        if self.comment["text"]:
            self.comment_textedit.setText(self.comment["text"])
            self.comment_textedit.setStyleSheet("font: 12pt")
        else:
            self.comment_textedit.setText("No comment")
            self.comment_textedit.setStyleSheet(
                "font: italic; font-size: 16px; color: grey"
            )
        self.comment_textedit.setReadOnly(True)

    def display_task_status(self):
        """
        Display the task status associated to the comment.
        """
        short_name = self.comment["task_status"]["short_name"]
        self.task_status.setText(short_name.upper())
        color = QtGui.QColor(self.color).lighter(110)
        background_color = QtGui.QColor(main_color)
        palette = self.task_status.palette()
        palette.setColor(
            QtGui.QPalette.Text, combine_colors(color, background_color, 0.9)
        )
        self.task_status.setPalette(palette)
        new_font = QtGui.QFont("Arial", 9)
        self.task_status.setFont(new_font)

    def display_profile_picture(self):
        """
        Add the profile picture of the sender.
        """
        url = os.path.join(
            "pictures",
            "thumbnails",
            "persons",
            self.comment["person"]["id"] + ".png",
        )
        try:
            data = get_file_data_from_url(url).content
            self.profile_picture = QtGui.QPixmap()
            self.profile_picture.loadFromData(data)
            icon = QtGui.QIcon(self.profile_picture)
        except:
            icon = get_icon_file("no_avatar.png")
        self.profile_picture_label.setPixmap(icon.pixmap(QtCore.QSize(40, 40)))

    def hide_button(self):
        """
        Hide temporarily the option button.
        """
        self.option.hide()

    def header(self):
        """
        Add a header painted with the color of the task status.
        """
        color = QtGui.QColor(self.color)

        self.color_header.setEnabled(False)
        darker_color = color.darker(170)
        pal = self.color_header.palette()
        pal.setColor(QtGui.QPalette.Button, darker_color)
        self.color_header.setAutoFillBackground(True)
        self.color_header.setPalette(pal)
        self.color_header.update()

        self.color_header_top.setEnabled(False)
        darker_color = color.darker(200)
        pal2 = self.color_header_top.palette()
        pal2.setColor(QtGui.QPalette.Button, darker_color)
        self.color_header_top.setAutoFillBackground(True)
        self.color_header_top.setPalette(pal2)
        self.color_header_top.update()

        self.color_header_bottom.setEnabled(False)
