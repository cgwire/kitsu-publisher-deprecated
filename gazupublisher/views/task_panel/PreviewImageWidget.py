
from Qt import QtWidgets, QtGui
from gazupublisher.utils.connection import (
    get_data_from_url,
)


class PreviewImageWidget(QtWidgets.QLabel):
    def __init__(self, url):
        QtWidgets.QLabel.__init__(self)
        self.url = url

    def fill_preview(self):
        data = get_data_from_url(self.url)
        pixmap = QtGui.QPixmap()
        pixmap.loadFromData(data)
        self.setPixmap(pixmap.scaledToHeight(100))

    def empty_preview(self):
        self.clear()
