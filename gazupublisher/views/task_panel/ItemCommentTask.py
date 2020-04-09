import os

from Qt import QtCore, QtGui, QtWidgets, QtCompat

from gazupublisher.utils.connection import get_host, get_data_from_url
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
        data = get_data_from_url(url).read()
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
        pal2.setColor(QtGui.QPalette.Button, color.darker())
        self.color_header_2.setPalette(pal2)
        self.color_header_2.update()


def main():
    import sys

    app = QtWidgets.QApplication(sys.argv)
    app.setApplicationDisplayName(
        QtCore.QCoreApplication.translate("Application", "Name")
    )
    from gazupublisher.utils.connection import connect_user, configure_host

    configure_host("http://localhost/api")
    connect_user("admin@example.com", "mysecretpassword")

    comment = {
        "id": "59bf2f0d-cdf3-44d8-9f5e-830d946c45b0",
        "created_at": "2020-03-31T08:44:49",
        "updated_at": "2020-03-31T09:03:39",
        "shotgun_id": None,
        "object_id": "b0555802-66be-4230-a8fb-cb972fb1a996",
        "object_type": "Task",
        "text": "seconde preview",
        "data": None,
        "checklist": None,
        "pinned": None,
        "task_status_id": "a78b28d7-0f89-422a-94f6-dc3f8a0d5a8d",
        "person_id": "4a4603a0-72a3-455a-8da0-aaa100d6cbd8",
        "preview_file_id": None,
        "type": "Comment",
        "person": {
            "first_name": "Super",
            "last_name": "Admin",
            "has_avatar": False,
            "id": "4a4603a0-72a3-455a-8da0-aaa100d6cbd8",
        },
        "task_status": {
            "name": "Todo",
            "short_name": "todo",
            "color": "#15f5f5",
            "id": "a78b28d7-0f89-422a-94f6-dc3f8a0d5a8d",
        },
        "previews": [
            {
                "id": "e9df2093-faa3-4ea5-bd15-b56242fe0bab",
                "revision": 2,
                "extension": "png",
                "annotations": None,
            },
            {
                "id": "bbd279d8-ae40-4572-a481-e8dca643d9e4",
                "revision": 2,
                "extension": "png",
                "annotations": None,
            },
        ],
    }

    window = QtWidgets.QMainWindow()

    list_widget = QtWidgets.QListWidget()
    item = QtWidgets.QListWidgetItem()
    # item.setSizeHint(QtCore.QSize(0, 150))

    widget = WidgetCommentTask(comment)
    list_widget.addItem(item)
    list_widget.setItemWidget(item, widget)
    list_widget.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    # class MyWidget(QtWidgets.QWidget):
    #  def enterEvent(self, evt):
    #     print('a')
    #
    # app = QtWidgets.QApplication([])
    # window = QtWidgets.QMainWindow()
    # window.resize(200, 200)
    # widget1 = MyWidget(window)
    # widget1.resize(100, 100)
    # widget1.setStyleSheet("background-color:#FFFFFF")
    # window.show()
    # app.exec_()
    main()
