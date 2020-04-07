import os

from Qt import QtWidgets, QtGui, QtCore

from gazupublisher.utils.connection import get_data_from_url, get_host
from gazupublisher.views.task_panel.PreviewWidget import PreviewWidget


class PreviewImageWidget(PreviewWidget):
    def __init__(self, preview_file):
        PreviewWidget.__init__(self, preview_file)

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
        self.layout().insertWidget(0, self.image_label)

    def fill_preview(self):

        data = get_data_from_url(self.url)
        pixmap = QtGui.QPixmap()
        pixmap.loadFromData(data.read())
        pixmap_ratio = pixmap.width() / pixmap.height()
        self.image_label.setPixmap(pixmap)
        self.image_label.setScaledContents(True)
        self.image_label.setFixedSize(
            self.toolbar_widget.sizeHint().width(),
            self.toolbar_widget.sizeHint().width() / pixmap_ratio
        )


    def add_buttons(self):
        self.next_button = ToolBarButton()
        self.previous_button = ToolBarButton()
        self.add_preview_button = ToolBarButton()

        self.toolbar_widget.layout().insertWidget(0, self.add_preview_button)
        self.toolbar_widget.layout().insertWidget(0, self.next_button)
        self.toolbar_widget.layout().insertWidget(0, self.previous_button)

    def clear_setup_media_widget(self):
        self.image_label.clear()


class ToolBarButton(QtWidgets.QPushButton):
    def __init__(self):
        QtWidgets.QPushButton.__init__(self)
        self.setMinimumWidth(25)
        self.setSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed
        )

