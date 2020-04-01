import os

from Qt import QtCore, QtGui, QtWidgets

from gazupublisher.utils.data import get_all_previews_for_task
from gazupublisher.utils.connection import (
    get_host,
    get_data_from_url,
)
from gazupublisher.utils.format import is_video

class ListPreviewTask(QtWidgets.QGraphicsScene):
    def __init__(self, task):
        QtWidgets.QGraphicsScene.__init__(self)
        self.task = task

        self.fill_datas()

        self.view = QtWidgets.QGraphicsView(self)
        self.view.show()

    def set_task(self, task):
        self.task = task

    def fill_datas(self):
        previews = get_all_previews_for_task(self.task)
        for preview in previews:
            url = os.path.join(
                get_host(),
                "movies" if is_video(preview) else "pictures",
                "previews",
                "preview-files",
                preview["id"] + "." + preview["extension"]
            )
            data = get_data_from_url(url)
            pixmap = QtGui.QPixmap()
            pixmap.loadFromData(data)
            item = QtWidgets.QGraphicsPixmapItem(pixmap)
            self.addItem(item)

    def empty(self):
        self.clear()

    def reload(self):
        self.empty()
        self.fill_datas()
