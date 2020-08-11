import os

from Qt import QtWidgets, QtGui, QtCore

from kitsupublisher.utils.connection import get_file_data_from_url
from kitsupublisher.views.task_panel.PreviewWidget import (
    PreviewWidget,
)
from kitsupublisher.exceptions import MediaNotSetUp

class CustomImageLabel(QtWidgets.QLabel):
    """
    QLabel to contain the preview. SizeHint overridden to match the panel width.
    """

    def __init__(self, parent):
        QtWidgets.QLabel.__init__(self)
        self.parent = parent
        self.setSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed
        )
        self.setAlignment(QtCore.Qt.AlignCenter)
        self.setFixedSize(self.sizeHint())
        self.setStyleSheet("QLabel { background-color: black }")

    def sizeHint(self):
        ratio = 16.0 / 9
        return QtCore.QSize(
            self.parent.desired_geometry.width(),
            self.parent.desired_geometry.width() / ratio,
        )


class ToolBarButton(QtWidgets.QPushButton):
    def __init__(self):
        QtWidgets.QPushButton.__init__(self)
        self.setMinimumWidth(25)
        self.setMaximumWidth(30)
        self.setSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed
        )


class PreviewImageWidget(PreviewWidget):
    def __init__(self, parent, preview_file):
        PreviewWidget.__init__(self, parent, preview_file)

    def complete_ui(self):
        self.preview_url = os.path.join(
            "pictures",
            "previews",
            "preview-files",
            self.preview_file["id"] + "." + self.preview_file["extension"],
        )
        self.add_buttons()
        self.image_label = CustomImageLabel(self.parent)
        self.fill_preview()
        self.preview_vertical_layout.insertWidget(
            0, self.image_label, QtCore.Qt.AlignCenter
        )

    def fill_preview(self):
        """
        Load preview image into label widget.
        """
        try:
            data = get_file_data_from_url(self.preview_url).content
            pixmap = QtGui.QPixmap()
            pixmap.loadFromData(data)
            pixmap = pixmap.scaled(
                self.image_label.size(), QtCore.Qt.KeepAspectRatio
            )
            self.image_label.setPixmap(pixmap)
        except:
            raise MediaNotSetUp()

    def add_buttons(self):
        self.next_button = ToolBarButton()
        self.previous_button = ToolBarButton()
        self.add_preview_button = ToolBarButton()

        self.toolbar_widget.layout().insertWidget(0, self.add_preview_button)
        self.toolbar_widget.layout().insertWidget(0, self.next_button)
        self.toolbar_widget.layout().insertWidget(0, self.previous_button)

        self.next_button.hide()
        self.previous_button.hide()
        self.add_preview_button.hide()

    def clear_setup_media_widget(self):
        """
        Clear the image.
        """
        self.image_label.clear()

    def get_height(self):
        """
        Return the height of the widget.
        """
        return (
            self.image_label.height()
            + 2 * self.preview_vertical_layout.spacing()
            + self.toolbar_widget.height()
        )
