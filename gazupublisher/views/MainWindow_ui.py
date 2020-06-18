# -*- coding: utf-8 -*-

from Qt import QtCore, QtWidgets

from gazupublisher.ui_data.table_headers import tab_columns

from gazupublisher.views.TasksTab import TasksTab
from gazupublisher.views.CustomToolBar import CustomToolBar
from gazupublisher.views.task_panel.TaskPanel import TaskPanel
from gazupublisher.utils.file import load_ui_file

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("window")

        load_ui_file("MainWindow.ui", self)

        self.setup_main_panel()

    def setup_main_panel(self):
        """
        Called at initialization.
        """

        self.table = TasksTab(self, tab_columns)
        self.toolbar = CustomToolBar(self)
        self.toolbar.setSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed
        )

        self.central_layout.addWidget(self.toolbar, 0, 0)
        self.central_layout.addWidget(self.table, 1, 0)

    def setup_task_panel(self, task):
        """
        Called at click on table.
        """
        if not hasattr(self, "task_panel"):
            self.table.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)

            self.task_panel = TaskPanel(self, task)

            self.central_layout.addWidget(self.task_panel, 0, 1, 2, 1)
        else:
            self.task_panel.update_datas(task)
            self.task_panel.reload()

    def reload(self):
        """
        Reload the two main panels.
        """
        if hasattr(self, "task_panel"):
            self.task_panel.reload()
        self.table.reload()
        self.table.resize_to_content()
