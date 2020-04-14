from Qt import QtCore, QtGui, QtWidgets

from gazupublisher.utils.data import get_all_comments_for_task
from gazupublisher.views.task_panel.ItemCommentTask import WidgetCommentTask


class ListCommentTask(QtWidgets.QListWidget):
    def __init__(self, parent, task):
        QtWidgets.QListWidget.__init__(self)
        self.parent = parent
        self.task = task
        self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.setSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Maximum
        )
        self.setFixedWidth(self.parent.desired_geometry.width())

        self.verticalScrollBar().setEnabled(True)
        self.horizontalScrollBar().setEnabled(False)
        self.model().rowsInserted.connect(self._recalcultate_height)
        self.model().rowsRemoved.connect(self._recalcultate_height)

    def set_task(self, task):
        self.task = task

    def fill_comments(self):
        list_comments = get_all_comments_for_task(self.task)
        for comment in list_comments:
            widget = WidgetCommentTask(comment)
            item = QtWidgets.QListWidgetItem()
            item.setFlags(item.flags() & QtCore.Qt.ItemIsSelectable)
            item.setSizeHint(widget.sizeHint())
            widget.setFixedWidth(self.parent.desired_geometry.width())

            self.addItem(item)
            self.setItemWidget(item, widget)

    def empty(self):
        self.clear()

    def reload(self, task):
        self.empty()
        self.set_task(task)
        self.fill_comments()

    def wheelEvent(self, event):
        """
        All the list is displayed, this function prevents parasite scrolling.
        """
        event.ignore()

    def _recalcultate_height(self):
        """
        Enable to display all the items in the list comment widget
        """
        h = sum([self.sizeHintForRow(i) for i in range(self.count())])
        self.setFixedHeight(h)
        self.updateGeometry()
