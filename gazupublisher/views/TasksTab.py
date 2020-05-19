import Qt.QtWidgets as QtWidgets
import Qt.QtCore as QtCore
import Qt.QtGui as QtGui

import gazupublisher.utils.data as utils_data
from gazupublisher.utils.other import combine_colors
from gazupublisher.views.TasksTabItem import TasksTabItem
from gazupublisher.ui_data.color import (
    main_color,
    table_alternate_color,
    text_color,
)
from gazupublisher.ui_data.ui_values import (
    height_table,
    row_height,
)


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
        self.setColumnCount(len(dict_cols))
        self.text_color = text_color
        self.create_header(dict_cols)

        self.tasks_to_do = utils_data.get_all_tasks_to_do()
        self.fill_tasks_tab(self.tasks_to_do)
        self.resize_to_content()
        self.activate_sort()

        self.item_delegate = StyleDelegateForQTableWidget(self)
        self.setItemDelegate(self.item_delegate)
        self.color_tab()

        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.setHorizontalScrollMode(QtWidgets.QAbstractItemView.ScrollPerPixel)

        self.manage_size()

        self.currentItemChanged.connect(self.on_current_item_changed)

    def manage_size(self):
        self.setFixedWidth(
            self.horizontalHeader().length() + self.verticalHeader().width() + 2
        )
        self.setSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed
        )

    def sizeHint(self):
        """
        Overriden size hint.
        """
        return QtCore.QSize(
            self.horizontalHeader().length() + self.verticalHeader().width(),
            height_table,
        )

    def create_header(self, dict_cols):
        """
        Create the header and set its visual aspect.
        """
        self.setHorizontalHeaderLabels(dict_cols.values())
        self.horizontalHeader().setHighlightSections(False)
        self.horizontalHeader().setSectionsClickable(False)
        stylesheet = (
            "::section{color:"
            + self.text_color
            + "; font-weight: bold; font-size: 18px}"
        )
        self.horizontalHeader().setStyleSheet(stylesheet)
        self.horizontalHeader().setDefaultAlignment(QtCore.Qt.AlignLeft)

    def fill_tasks_tab(self, tasks):
        """
        Fill the table with the given tasks.
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
                item = TasksTabItem(self, nb_row, nb_col, task, task_attribute)
                self.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
                self.setItem(nb_row, nb_col, item)
            self.setRowHeight(nb_row, row_height)

    def reload(self):
        """
        Delete the datas of the table, then fills with the new ones.
        """
        self.currentItemChanged.disconnect()
        self.empty()
        self.deactivate_sort()

        self.create_header(self.tab_columns)
        self.tasks_to_do = utils_data.get_all_tasks_to_do()
        self.fill_tasks_tab(self.tasks_to_do)
        self.resize_to_content()

        self.activate_sort()

        self.color_tab()

        self.currentItemChanged.connect(self.on_current_item_changed)

    def empty(self):
        """
        Empty the table.
        """
        self.clear()
        self.setRowCount(0)

    def resize_to_content(self):
        """
        Resize the table to its contents.
        """
        self.resizeColumnsToContents()

    def activate_sort(self):
        """
        Activate the sorting of the table.
        """
        self.setSortingEnabled(True)
        self.sortItems(0, QtCore.Qt.AscendingOrder)

    def deactivate_sort(self):
        """
        Deactivate the sorting of the table.
        """
        self.setSortingEnabled(False)

    def on_current_item_changed(self, current_item, previous_item):
        """
        On table item click, call the initialization/update of the right panel.
        Does nothing if the row is the same.
        """
        if (
            previous_item
            and current_item
            and previous_item.task["id"] != current_item.task["id"]
        ):
            self.window.setup_task_panel(current_item.task)

    def color_tab(self):
        """
        Paint the items of the table with alternate nuances of grey.
        """
        for nb_row in range(self.rowCount()):
            row_color = (
                QtGui.QColor(main_color)
                if nb_row % 2 == 0
                else QtGui.QColor(table_alternate_color)
            )
            for nb_col in range(self.columnCount() - 1):
                item = self.item(nb_row, nb_col)
                item_color = row_color
                if item.is_bg_colored:
                    item_color = combine_colors(
                        row_color, item.background().color()
                    )
                brush = QtGui.QBrush(item_color)
                item.setBackground(brush)
