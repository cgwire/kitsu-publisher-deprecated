# -*- coding: utf-8 -*-
from gazupublisher import resources_rc  # needed to load assets

from Qt import QtCore, QtWidgets

from gazupublisher.views.TasksTab import TasksTab
from gazupublisher.views.CustomToolBar import CustomToolBar
from .table_headers import tab_columns

from gazupublisher.views.TasksTab import TasksTab
from gazupublisher.views.CustomToolBar import CustomToolBar
from gazupublisher.views.ListCommentTask import ListCommentTask
from gazupublisher.views.ListPreviewTask import ListPreviewTask


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

        self.setup_left()

        MainWindow.setCentralWidget(self.central_widget)

        self.fitToTable()

    def setup_left(self):
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

    # def setup_right(self, task):
    #     """
    #     Called at click on table.
    #     """
    #
    #     if not hasattr(self, "list_widget"):
    #         self.list_widget = ListCommentTask(task)
    #         self.list_widget.show()
    #         self.horizontal_layout.addWidget(self.list_widget)
    #     else:
    #         self.list_widget.set_task(task)
    #         self.list_widget.reload()

    def setup_right(self, task):
        """
        Called at click on table.
        """

        if not hasattr(self, "list_widget"):
            self.list_widget = ListPreviewTask(task)
            self.horizontal_layout.addWidget(self.list_widget.view)
        else:
            self.list_widget.set_task(task)
            self.list_widget.reload()


    def fitToTable(self):
        self.table.setFixedSize(
            self.table.horizontalHeader().length()
            + self.table.verticalHeader().width(),
            self.table.verticalHeader().length()
            + self.table.horizontalHeader().height(),
        )
