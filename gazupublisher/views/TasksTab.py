import Qt.QtWidgets as QtWidgets
import Qt.QtCore as QtCore
import Qt.QtGui as QtGui

import gazupublisher.utils.data as utils_data
from gazupublisher.utils.other import combine_colors
from .CommentWindow import CommentWindow
from gazupublisher.views.CommentButton import CommentButton
from gazupublisher.views.TasksTabItem import TasksTabItem


class StyleDelegateForQTableWidget(QtWidgets.QStyledItemDelegate):
    """
    Class overriding QTableWidgetItem color policy, to obtain
    transparency when a row is selected
    """

    def __init__(self, parent):
        QtWidgets.QStyledItemDelegate.__init__(self, parent)
        self.parent = parent
        self.color_default = QtGui.QColor("#5e60ba")

    def paint(self, painter, option, index):
        if option.state & QtWidgets.QStyle.State_Selected:
            option.palette.setColor(
                QtGui.QPalette.HighlightedText,
                QtGui.QColor(self.parent.text_color),
            )
            color = combine_colors(
                self.color_default, self.background(option, index)
            )
            option.palette.setColor(QtGui.QPalette.Highlight, color)
        QtWidgets.QStyledItemDelegate.paint(self, painter, option, index)

    def background(self, option, index):
        item = self.parent.itemFromIndex(index)
        if item:
            if item.background() != QtGui.QBrush():
                return item.background().color()
        if self.parent.alternatingRowColors():
            if index.row() % 2 == 1:
                return option.palette.color(QtGui.QPalette.AlternateBase)
        return option.palette.color(QtGui.QPalette.Base)


class TasksTab(QtWidgets.QTableWidget):
    """
    The table containing all the tasks to do for the current user.
    The columns of the array are set manually at instantiation.
    """

    def __init__(self, window, dict_cols):
        QtWidgets.QTableWidget.__init__(self)

        self.window = window
        self.tab_columns = dict_cols
        self.list_ids = list(dict_cols.keys())
        self.setColumnCount(len(dict_cols) + 1)

        self.item_delegate = StyleDelegateForQTableWidget(self)
        self.setItemDelegate(self.item_delegate)

        self.setSizePolicy(
            QtWidgets.QSizePolicy.Ignored, QtWidgets.QSizePolicy.Ignored
        )

        self.text_color = "#eee"
        self.create_header(dict_cols)

        self.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)

        self.current_item = None
        self.currentItemChanged.connect(self.on_current_item_changed)

        self.tasks_to_do = utils_data.get_all_tasks_to_do()
        self.fill_tab(self.tasks_to_do)
        self.resize_to_content()
        self.sort()

    def create_header(self, dict_cols):
        """
        Create the header and set its visual aspect.
        """
        self.setHorizontalHeaderLabels(dict_cols.values())
        self.horizontalHeader().setHighlightSections(False)
        stylesheet = (
            "::section{color:" + self.text_color + "; font-weight: bold;}"
        )
        self.horizontalHeader().setStyleSheet(stylesheet)

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
            for nb_col, task_attribute in enumerate(self.list_ids):
                assert task_attribute in task, (
                    "The attribute "
                    + task_attribute
                    + " doesn't belong to the attributes of a "
                    "gazu task object "
                )
                if isinstance(task[task_attribute], dict):
                    assert task_attribute == "last_comment", (
                        "Undefined behaviour, "
                        "maybe following the "
                        "addition of a new "
                        "attribute ?"
                    )
                    if task[task_attribute]:
                        item = TasksTabItem(
                            self,
                            nb_row,
                            nb_col,
                            task,
                            task_attribute,
                            task[task_attribute]["text"],
                        )
                    else:
                        item = TasksTabItem(
                            self, nb_row, nb_col, task, task_attribute
                        )
                else:
                    item = TasksTabItem(
                        self,
                        nb_row,
                        nb_col,
                        task,
                        task_attribute,
                        task[task_attribute],
                    )
                item.setTextAlignment(QtCore.Qt.AlignCenter)
                self.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
                self.setItem(nb_row, nb_col, item)

    def add_comment_buttons(self):
        """
        Add the comment buttons in the final column
        """
        for nb_row, task in enumerate(self.tasks_to_do):

            def open_comment_window(container, button, task):
                def open():
                    """
                    Called for each click on the comment button
                    """
                    button.comment_window = CommentWindow(task, container)
                    button.comment_window.exec_()

                return open

            button = CommentButton(None, "Comment")
            button.clicked.connect(open_comment_window(self, button, task))
            self.setCellWidget(nb_row, self.columnCount() - 1, button)

    def reload(self):
        """
        Delete the datas of the table, then asks for the new ones
        """
        self.currentItemChanged.disconnect()
        self.empty()
        self.tasks_to_do = utils_data.get_all_tasks_to_do()
        self.fill_tab(self.tasks_to_do)

        self.resize_to_content()
        self.sort()
        self.currentItemChanged.connect(self.on_current_item_changed)

    def empty(self):
        """
        Empty the table. The column headers are NOT deleted
        """
        self.setRowCount(0)

    def resize_to_content(self):
        """
        Resize the table to its contents.
        """
        self.resizeColumnsToContents()
        self.resizeRowsToContents()
        self.setColumnWidth(8, 200)

    def sort(self):
        """
        Sort the table by given attribute.
        """
        if hasattr(self.window, "toolbar"):
            task_attribute = self.window.toolbar.get_current_sort_attribute()
            column_name = self.tab_columns[task_attribute]
            for i in range(self.columnCount()):
                current_header = self.horizontalHeaderItem(i)
                if current_header and current_header.text() == column_name:
                    index = i
                    break
            self.sortItems(index, QtCore.Qt.AscendingOrder)

    def on_current_item_changed(self, current_item, previous_item):
        """
        On table item click, call the initialization/update of the right panel.
        Does nothing if the row is the same.
        """
        if not previous_item or (
            previous_item and previous_item.row() != current_item.row()
        ):
            self.window.setup_task_panel(current_item.task)
