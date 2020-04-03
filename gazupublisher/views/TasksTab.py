import Qt.QtWidgets as QtWidgets
import Qt.QtCore as QtCore
import Qt.QtGui as QtGui

import gazupublisher.utils.data as utils_data
from .CommentWindow import CommentWindow
from gazupublisher.views.CommentButton import CommentButton
from gazupublisher.views.TasksTabItem import TasksTabItem


class TasksTab(QtWidgets.QTableWidget):
    """
    The table containing all the tasks to do for the current user.
    The columns of the array are set manually at instantiation.
    """

    def __init__(self, window, dict_cols):
        QtWidgets.QTableWidget.__init__(self)

        class StyleDelegateForQTableWidget(QtWidgets.QStyledItemDelegate):
            """
            Class overriding QTableWidgetItem color policy, to obtain
            transparency when a row is selected
            """

            color_default = QtGui.QColor("#aaedff")

            def paint(self, painter, option, index):
                if option.state & QtWidgets.QStyle.State_Selected:
                    option.palette.setColor(
                        QtGui.QPalette.HighlightedText, QtCore.Qt.black
                    )
                    color = self.combine_colors(
                        self.color_default, self.background(option, index)
                    )
                    option.palette.setColor(QtGui.QPalette.Highlight, color)
                QtWidgets.QStyledItemDelegate.paint(
                    self, painter, option, index
                )

            def background(self, option, index):
                item = self.parent().itemFromIndex(index)
                if item:
                    if item.background() != QtGui.QBrush():
                        return item.background().color()
                if self.parent().alternatingRowColors():
                    if index.row() % 2 == 1:
                        return option.palette.color(
                            QtGui.QPalette.AlternateBase
                        )
                return option.palette.color(QtGui.QPalette.Base)

            @staticmethod
            def combine_colors(c1, c2):
                c3 = QtGui.QColor()
                c3.setRed((c1.red() + c2.red()) / 2)
                c3.setGreen((c1.green() + c2.green()) / 2)
                c3.setBlue((c1.blue() + c2.blue()) / 2)
                return c3

        self.item_delegate = StyleDelegateForQTableWidget(self)
        self.setItemDelegate(self.item_delegate)

        self.setSizePolicy(QtWidgets.QSizePolicy.Ignored, QtWidgets.QSizePolicy.Ignored)


        self.window = window
        self.tab_columns = dict_cols
        self.list_ids = list(dict_cols.keys())
        self.setColumnCount(len(dict_cols) + 1)
        self.setHorizontalHeaderLabels(dict_cols.values())
        self.horizontalHeader().setHighlightSections(False)

        self.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)

        self.current_item = None
        self.currentItemChanged.connect(self.on_click)

        self.tasks_to_do = utils_data.get_all_tasks_to_do()
        self.fill_tab(self.tasks_to_do)
        self.resize_to_content()
        self.sort()

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
                assert col in task, (
                    "The attribute "
                    + col
                    + " doesn't belong to the attributes of a "
                    "gazu task object "
                )
                if isinstance(task[col], dict):
                    assert col == "last_comment", (
                        "Undefined behaviour, "
                        "maybe following the "
                        "addition of a new "
                        "attribute ?"
                    )
                    if task[col]:
                        item = TasksTabItem(
                            task, task[col]["text"]
                        )
                    else:
                        item = TasksTabItem(task)
                else:
                    item = TasksTabItem(task, task[col])
                item.setTextAlignment(QtCore.Qt.AlignCenter)
                self.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
                self.paint_tab_item(item, task, col)
                self.setItem(nb_row, nb_col, item)

    def paint_tab_item(self, item, task, task_attribute):
        color = "#ffffff"
        if task_attribute == "task_type_name":
            color = task["task_type_color"]
        elif (
            task_attribute == "task_status_short_name"
            or task_attribute == "task_status_name"
        ):
            color = task["task_status_color"]
        brush = QtGui.QBrush(QtGui.QColor(color))
        item.setBackground(brush)

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
        self.empty()

        self.tasks_to_do = utils_data.get_all_tasks_to_do()
        self.fill_tab(self.tasks_to_do)

        self.resize_to_content()
        self.sort()

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

    def on_click(self, current_item, previous_item):
        """
        On table item click, call the initialization/update of the right panel.
        Does nothing if the row is the same.
        """
        if not previous_item or previous_item.row() != current_item.row():
            self.window.setup_task_panel(current_item.task)
