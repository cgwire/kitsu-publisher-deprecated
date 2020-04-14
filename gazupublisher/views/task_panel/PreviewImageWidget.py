import os

from Qt import QtWidgets, QtGui, QtCore

from gazupublisher.utils.connection import get_file_data_from_url, get_host
from gazupublisher.views.task_panel.PreviewWidget import PreviewWidget


class PreviewImageWidget(PreviewWidget):
    def __init__(self, parent, preview_file):
        PreviewWidget.__init__(self, parent, preview_file)

    def complete_ui(self):
        self.url = os.path.join(
            get_host(),
            "pictures",
            "previews",
            "preview-files",
            self.preview_file["id"] + "." + self.preview_file["extension"],
        )
        self.add_buttons()
        self.image_label = QtWidgets.QLabel()
        self.fill_preview()
        self.preview_vertical_layout.insertWidget(
            0, self.image_label, QtCore.Qt.AlignCenter
        )

    def fill_preview(self):
        """
        Load preview image into label widget and set layout settings.
        """
        data = get_file_data_from_url(self.url)
        pixmap = QtGui.QPixmap()
        pixmap.loadFromData(data.read())

        frame_size = QtCore.QSize(
            self.desired_geometry.width(), self.desired_geometry.height()
        )
        pixmap = pixmap.scaled(frame_size, QtCore.Qt.KeepAspectRatio)
        self.image_label.setPixmap(pixmap)
        self.image_label.resize(pixmap.size())
        self.image_label.setStyleSheet("QLabel { background-color: black }")
        self.image_label.setAlignment(QtCore.Qt.AlignCenter)

    def add_buttons(self):
        self.next_button = ToolBarButton()
        self.previous_button = ToolBarButton()
        self.add_preview_button = ToolBarButton()

        self.toolbar_widget.layout().insertWidget(0, self.add_preview_button)
        self.toolbar_widget.layout().insertWidget(0, self.next_button)
        self.toolbar_widget.layout().insertWidget(0, self.previous_button)

    def clear_setup_media_widget(self):
        self.image_label.clear()

    def get_height(self):
        return (
            self.toolbar_widget.geometry().height()
            + self.image_label.frameGeometry().height()
        )


class ToolBarButton(QtWidgets.QPushButton):
    def __init__(self):
        QtWidgets.QPushButton.__init__(self)
        self.setMinimumWidth(25)
        self.setMaximumWidth(30)
        self.setSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed
        )
