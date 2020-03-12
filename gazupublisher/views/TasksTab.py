import sys
import gazu

import Qt.QtWidgets as QtWidgets
import Qt.QtCore as QtCore
from .CommentWindow import CommentWindow

class TasksTab(QtWidgets.QTableWidget):
    """
    The table containing all the tasks to do for the current user.
    The columns of the array are set manually at instanciation.
    """
    def __init__(self, dict_cols, parent=None):
        QtWidgets.QTableWidget.__init__(self, parent)
        self.list_ids = list(dict_cols.keys())
        self.setColumnCount(len(dict_cols)+1)
        self.setHorizontalHeaderLabels(dict_cols.values())
        self.fill_tab()

    def fill_tab(self):
        """
        Fill the tab with the tasks.
        """
        try:
            self.tasks_to_do = gazu.user.all_tasks_to_do()
        except:
            raise ConnectionError("Could not get user tasks")

        self.fill_tasks_tab(self.tasks_to_do)
        self.add_comment_buttons()
        self.resizeColumnsToContents()

    def fill_tasks_tab(self, tasks):
        """
        Fill the table with the given tasks
        """
        for nb_row, task in enumerate(tasks):
            current_row_nb = self.rowCount() + 1
            self.setRowCount(current_row_nb)
            for nb_col, col in enumerate(self.list_ids):
                assert col in task, "A given attribute doesn't belong to the attributes of a gazu task object "
                if isinstance(task[col], dict):
                    assert col == "last_comment", "Undefined behaviour, " \
                                                  "maybe following the addition of a new attribute ?"
                    if task[col]:
                        item = QtWidgets.QTableWidgetItem(task[col]["text"])
                    else:
                        item = QtWidgets.QTableWidgetItem()
                else:
                    item = QtWidgets.QTableWidgetItem(task[col])
                item.setTextAlignment(4)
                item.setFlags(QtCore.Qt.ItemIsEnabled)

                self.setItem(nb_row, nb_col, item)

    def add_comment_buttons(self):
        """
        Add the comment buttons in the final column
        """
        for nb_row, task in enumerate(self.tasks_to_do):

            button = QtWidgets.QPushButton("Comment")
            comment_window = CommentWindow(task, self)
            comment_window.hide()
            button.clicked.connect(self.open_comment_window(comment_window))
            self.setCellWidget(nb_row, self.columnCount() - 1, button)


    def open_comment_window(self, comment_window):
        def open():
            comment_window.show()
        return open

    def reload(self):
        """
        Delete the datas of the table, then asks for the new ones
        """
        self.empty()
        self.get_tasks_tab()

    def empty(self):
        """
        Empty the table. The column headers are NOT deleted
        """
        self.setRowCount(0)
