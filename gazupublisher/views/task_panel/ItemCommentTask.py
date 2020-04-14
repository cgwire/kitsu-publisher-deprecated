import os

from Qt import QtCore, QtGui, QtWidgets, QtCompat

from gazupublisher.utils.connection import get_host, get_file_data_from_url
from gazupublisher.utils.other import format_date


class WidgetCommentTask(QtWidgets.QWidget):
    def __init__(self, comment):
        super(WidgetCommentTask, self).__init__()
        self.comment = comment
        self.color = self.comment["task_status"]["color"]
        self.setup_ui()

    def setup_ui(self):
        QtCompat.loadUi("../resources/views/CommentWidget.ui", self)
        self.setLayout(self.gridLayout)

        self.comment_textedit = self.findChild(QtWidgets.QTextEdit, "comment_textedit")
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
        self.color_header_2 = self.findChild(
            QtWidgets.QPushButton, "color_header_2"
        )
        self.color_header_3 = self.findChild(
            QtWidgets.QPushButton, "color_header_3"
        )

        self.display_profile_picture()
        self.display_task_status()
        self.display_sender_name()
        self.display_creation_date()
        self.display_comment()
        self.header()

    def display_sender_name(self):
        name = self.comment["person"]["first_name"] + " " + self.comment["person"]["last_name"]
        self.sender_name.setStyleSheet("font-weight: bold")
        self.sender_name.setText(name)

    def display_creation_date(self):
        creation_date = format_date(self.comment["created_at"])
        self.sender_name.setStyleSheet("font-weight: bold")
        self.date.setText(creation_date)

    def display_comment(self):
        self.comment_textedit.setText(self.comment["text"])
        self.comment_textedit.setReadOnly(True)

    def display_task_status(self):
        """
        Display the task status.
        """
        short_name = self.comment["task_status"]["short_name"]
        self.task_status.setText(short_name.upper())
        color = QtGui.QColor(self.color) if short_name != "todo" else QtGui.QColor("grey")
        palette = self.task_status.palette()
        palette.setColor(QtGui.QPalette.Text, color)
        self.task_status.setPalette(palette)
        new_font = QtGui.QFont("Arial", 8)
        self.task_status.setFont(new_font)

    def display_profile_picture(self):
        """
        Add the profile picture of the sender.
        """
        url = os.path.join(
            get_host(),
            "pictures",
            "thumbnails",
            "persons",
            self.comment["person"]["id"] + ".png",
        )
        data = get_file_data_from_url(url).read()
        self.profile_picture = QtGui.QPixmap()
        self.profile_picture.loadFromData(data)
        icon = QtGui.QIcon(self.profile_picture)
        self.profile_picture_label.setPixmap(icon.pixmap(QtCore.QSize(30, 30)))


    def header(self):
        """
        Add a header painted with the color of the task status.
        """
        short_name = self.comment["task_status"]["short_name"]
        color = QtGui.QColor(self.color) if short_name != "todo" \
            else QtGui.QColor("grey")

        self.color_header.setEnabled(False)
        pal = self.color_header.palette()
        pal.setColor(QtGui.QPalette.Button, color)
        self.color_header.setAutoFillBackground(True)
        self.color_header.setPalette(pal)
        self.color_header.update()

        self.color_header_2.setEnabled(False)
        pal2 = self.color_header_2.palette()
        darker_color = color.darker(200)
        pal2.setColor(QtGui.QPalette.Button, darker_color)
        self.color_header_2.setAutoFillBackground(True)
        self.color_header_2.setPalette(pal2)
        self.color_header_2.update()

        self.color_header_3.setEnabled(False)
