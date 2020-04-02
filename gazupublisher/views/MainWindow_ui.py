# -*- coding: utf-8 -*-

from Qt import QtCore, QtWidgets

from .table_headers import tab_columns

from gazupublisher.views.TasksTab import TasksTab
from gazupublisher.views.CustomToolBar import CustomToolBar
from gazupublisher.views.task_panel.TaskPanel import TaskPanel
from views.task_panel.ListPreviewTask import ListPreviewTask


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("window")

        self.central_widget = QtWidgets.QWidget(MainWindow)
        self.central_widget.setObjectName("centralWidget")

        self.horizontal_layout = QtWidgets.QHBoxLayout(self.central_widget)
        self.horizontal_layout.setObjectName("horizontalLayout")

        self.left_widget = QtWidgets.QWidget()
        self.right_widget = QtWidgets.QWidget()
        self.left_widget.setObjectName("left_widget")
        self.right_widget.setObjectName("right_widget")
        self.horizontal_layout.addWidget(self.left_widget)
        self.horizontal_layout.addWidget(self.right_widget)

        self.setup_main_panel()

        MainWindow.setCentralWidget(self.central_widget)

        self.fitToTable()

    def setup_main_panel(self):
        """
        Called at initialization.
        """

        self.vertical_layout = QtWidgets.QVBoxLayout(self.left_widget)
        self.vertical_layout.setObjectName("vertical_layout")

        self.table = TasksTab(self, tab_columns)
        self.table.verticalHeader().sectionResized.connect(self.fitToTable)
        self.table.horizontalHeader().sectionResized.connect(self.fitToTable)
        self.table.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.table.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.table.show()

        self.toolbar = CustomToolBar(self)
        self.toolbar.show()

        self.vertical_layout.addWidget(self.toolbar)
        self.vertical_layout.addWidget(self.table)

    def setup_task_panel(self, task):
        """
        Called at click on table.
        """

        if not hasattr(self, "task_panel"):
            self.task_panel = TaskPanel(self, task)
            self.horizontal_layout.addWidget(self.task_panel)
        else:
            self.task_panel.update_datas(task)
            self.task_panel.reload()


    def fitToTable(self):
        self.table.setFixedSize(
            self.table.horizontalHeader().length()
            + self.table.verticalHeader().width(),
            self.table.verticalHeader().length()
            + self.table.horizontalHeader().height(),
        )
