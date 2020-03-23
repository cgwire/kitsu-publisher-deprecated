import sys
import gazu
import gazupublisher.config as config

import Qt.QtWidgets as QtWidgets
import Qt.QtCore as QtCore

import gazupublisher.utils.data as utils_data
from .CommentWindow import CommentWindow

class TasksTab(QtWidgets.QTableWidget):
    """
    The table containing all the tasks to do for the current user.
    The columns of the array are set manually at instanciation.
    """
    def __init__(self, window, dict_cols, sort_attribute=None):
        QtWidgets.QTableWidget.__init__(self)
        self.window = window
        self.tab_columns = dict_cols
        self.list_ids = list(dict_cols.keys())
        self.setColumnCount(len(dict_cols)+1)
        self.setHorizontalHeaderLabels(dict_cols.values())
        self.tasks_to_do = utils_data.get_all_tasks_to_do()
        self.fill_tab(self.tasks_to_do)
        self.resize_to_content()
        self.sort_attribute = sort_attribute
        if not self.sort_attribute:
            self.sort_attribute = self.list_ids[0]
        self.sort(self.sort_attribute)

    def fill_tab(self, tasks):
        """
        Fill the tab with all the elements.
        """

        self.fill_tasks_tab(tasks)
        self.add_comment_buttons()

    def fill_tasks_tab(self, tasks):
        """
        Fill the table with the given tasks
        """
        for nb_row, task in enumerate(tasks):
            current_row_nb = self.rowCount() + 1
            self.setRowCount(current_row_nb)
            for nb_col, col in enumerate(self.list_ids):
                assert col in task, "The attribute " + col + " doesn't belong to the attributes of a gazu task object "
                if isinstance(task[col], dict):
                    assert col == "last_comment", "Undefined behaviour, " \
                                                  "maybe following the addition of a new attribute ?"
                    if task[col]:
                        item = QtWidgets.QTableWidgetItem(task[col]["text"])
                    else:
                        item = QtWidgets.QTableWidgetItem()
                else:
                    item = QtWidgets.QTableWidgetItem(task[col])
                item.setTextAlignment(QtCore.Qt.AlignCenter)
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
            comment_window.le.clear()
            comment_window.show()
        return open

    def reload(self):
        """
        Delete the datas of the table, then asks for the new ones
        """
        self.empty()
        self.tasks_to_do = utils_data.get_all_tasks_to_do()
        self.fill_tab(self.tasks_to_do)
        self.resize_to_content()
        if not self.sort_attribute:
            self.sort_attribute = self.list_ids[0]
        self.sort(self.sort_attribute)

    def empty(self):
        """
        Empty the table. The column headers are NOT deleted
        """
        self.setRowCount(0)

    def resize_to_content(self):
        """
        Resize the table to its contents
        """
        self.resizeColumnsToContents()
        self.resizeRowsToContents()

    def sort(self, task_attribute):
        """
        Sort the table by given attribute
        """
        column_name = self.tab_columns[task_attribute]
        for i in range(self.columnCount()):
            current_header = self.horizontalHeaderItem(i)
            if current_header and current_header.text() == column_name:
                index = i
                break
        self.sortItems(index, QtCore.Qt.AscendingOrder)