# -*- coding: utf-8 -*-

from Qt import QtCore, QtWidgets

from ui_data.table_headers import tab_columns

from gazupublisher.views.TasksTab import TasksTab
from gazupublisher.views.CustomToolBar import CustomToolBar
from gazupublisher.views.task_panel.TaskPanel import TaskPanel
from gazupublisher.ui_data.color import main_color


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("window")

        self.central_widget = QtWidgets.QWidget(MainWindow)

        self.main_layout = QtWidgets.QHBoxLayout(self.central_widget)
        self.main_widget = QtWidgets.QWidget()
        self.main_layout.addWidget(self.main_widget)

        self.setup_main_panel()

        MainWindow.setCentralWidget(self.central_widget)

        self.fit_to_table()

    def setup_main_panel(self):
        """
        Called at initialization.
        """

        self.vertical_layout = QtWidgets.QVBoxLayout(self.main_widget)
        self.vertical_layout.setObjectName("vertical_layout")

        self.table = TasksTab(self, tab_columns)
        self.table.show()

        self.toolbar = CustomToolBar(self)
        self.toolbar.setSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed
        )
        self.toolbar.show()

        self.vertical_spacer = QtWidgets.QSpacerItem(
            20,
            40,
            QtWidgets.QSizePolicy.Minimum,
            QtWidgets.QSizePolicy.Expanding,
        )

        self.vertical_layout.addWidget(self.toolbar)
        self.vertical_layout.addWidget(self.table)
        self.vertical_layout.addItem(self.vertical_spacer)

    def setup_task_panel(self, task):
        """
        Called at click on table.
        """
        if not hasattr(self, "task_panel"):
            self.scroll_area = QtWidgets.QScrollArea()
            self.task_panel = TaskPanel(self, task)
            self.scroll_area.setWidget(self.task_panel)
            self.scroll_area.setHorizontalScrollBarPolicy(
                QtCore.Qt.ScrollBarAlwaysOff
            )
            self.scroll_area.setVerticalScrollBarPolicy(
                QtCore.Qt.ScrollBarAlwaysOff
            )
            self.scroll_area.setSizePolicy(
                QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Maximum
            )

            self.horizontal_spacer = QtWidgets.QSpacerItem(
                20,
                40,
                QtWidgets.QSizePolicy.Expanding,
                QtWidgets.QSizePolicy.Minimum,
            )

            self.main_layout.addWidget(self.scroll_area)
            self.main_layout.addItem(self.horizontal_spacer)

        else:
            self.task_panel.update_datas(task)
            self.task_panel.reload()

    def fit_to_table(self):
        self.table.setFixedSize(
            self.table.horizontalHeader().length()
            + self.table.verticalHeader().width(),
            self.table.verticalHeader().length()
            + self.table.horizontalHeader().height(),
        )
