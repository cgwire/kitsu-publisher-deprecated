import os

from Qt import QtWidgets, QtGui, QtCore

from gazupublisher.utils.connection import get_file_data_from_url, get_host
from gazupublisher.views.task_panel.PreviewWidget import PreviewWidget


class CustomImageLabel(QtWidgets.QLabel):
    """
    QLabel to contain the preview. SizeHint overriden to match the panel width
    """

    def __init__(self, parent):
        QtWidgets.QLabel.__init__(self)
        self.parent = parent
        self.setSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed
        )
        self.setAlignment(QtCore.Qt.AlignCenter)
        self.setStyleSheet("QLabel { background-color: black }")

    def sizeHint(self):
        ratio = 16 / 9
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
        self.url = os.path.join(
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
        data = get_file_data_from_url(self.url).content
        pixmap = QtGui.QPixmap()
        pixmap.loadFromData(data)
        pixmap = pixmap.scaled(
            self.image_label.sizeHint(), QtCore.Qt.KeepAspectRatio
        )
        self.image_label.setPixmap(pixmap)

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
        self.image_label.clear()

    def get_height(self):
        return (
            self.toolbar_widget.sizeHint().height()
            + self.image_label.sizeHint().height()
        )
