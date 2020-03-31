from Qt import QtCore, QtGui, QtWidgets

from gazupublisher.utils.data import get_all_previews_for_task


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
        pixmap = QtGui.QPixmap("../resources/icons/refresh.ico")
        preview_files = get_all_previews_for_task(self.task)
        item = QtWidgets.QGraphicsPixmapItem(pixmap)
        self.addItem(item)
        # self.preview_id = self.task["entity_preview_file_id"]
        # import gazu
        # preview_files = gazu.files.get_all_preview_files_for_task(self.task)
        # gazu.files.download_preview_file(self.preview_id, "../resources/test/TEST.jpg")
        # self.addText(self.preview_id)

    def empty(self):
        self.clear()

    def reload(self):
        self.empty()
        self.fill_datas()
