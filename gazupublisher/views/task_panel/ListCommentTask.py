from Qt import QtCore, QtGui, QtWidgets

from gazupublisher.utils.data import get_all_comments_for_task


class ListCommentTask(QtWidgets.QListWidget):
    def __init__(self, task):
        QtWidgets.QListWidget.__init__(self)
        self.task = task
        self.fill_comments()

    def set_task(self, task):
        self.task = task

    def fill_comments(self):
        list_comments = get_all_comments_for_task(self.task)
        for comment in list_comments:
            text_comment = comment["text"]
            list_item = QtWidgets.QListWidgetItem(text_comment)
            self.addItem(list_item)

    def empty(self):
        self.clear()

    def reload(self):
        self.empty()
        self.fill_comments()
