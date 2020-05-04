from Qt import QtCore, QtGui, QtWidgets

from gazupublisher.utils.data import get_all_comments_for_task
from gazupublisher.views.task_panel.ItemCommentTask import WidgetCommentTask


class ListCommentTask(QtWidgets.QListWidget):
    """
    A widget to display the history of comments.
    """

    def __init__(self, parent, task):
        QtWidgets.QListWidget.__init__(self)
        self.parent = parent
        self.task = task
        self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.setSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Ignored
        )
        self.setFixedWidth(self.parent.desired_geometry.width() + 2)
        self.height = 0

        self.verticalScrollBar().setEnabled(True)
        self.horizontalScrollBar().setEnabled(False)
        self.fill_comments()

        self.setFrameShape(QtWidgets.QFrame.NoFrame)

    def set_task(self, task):
        self.task = task

    def fill_comments(self):
        """
        Fill the widget with the comment items.
        """
        list_comments = get_all_comments_for_task(self.task)
        for comment in list_comments:
            widget = WidgetCommentTask(comment)
            item = QtWidgets.QListWidgetItem()
            item.setFlags(item.flags() & QtCore.Qt.ItemIsSelectable)
            item.setSizeHint(QtCore.QSize(widget.width(), widget.height()))
            widget.setFixedWidth(self.parent.desired_geometry.width())

            self.height += widget.height()
            self.addItem(item)
            self.setItemWidget(item, widget)
        self._recalcultate_height()

    def empty(self):
        """
        Empty the list.
        """
        self.clear()

    def reload(self, task):
        """
        Reload the whole widget.
        """
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
        Enable to display all the items in the list comment widget.
        The list widget must take all space even when there is few or zero
        items ; we look for the space taken by the other widgets and set height
        accordingly.
        """
        min_height = self.parent.height() - (
            self.parent.post_comment_widget.geometry().height()
            + self.parent.preview_widget.get_height()
        )
        self.setFixedHeight(max(self.height, min_height))
