# -*- coding: utf-8 -*-

from Qt import QtCore, QtWidgets, QtGui

from kitsupublisher.ui_data.table_headers import tab_columns

from kitsupublisher.views.TasksTab import TasksTab
from kitsupublisher.views.task_panel.TaskPanel import TaskPanel
from kitsupublisher.views.CustomToolBar import CustomToolBar
from kitsupublisher.utils.file import load_ui_file

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("window")

        load_ui_file("MainWindow.ui", self)
        self.main_layout = self.findChild(QtWidgets.QLayout, "main_layout")
        self.central_layout = self.findChild(QtWidgets.QLayout, "central_layout")

        self.setup_main_panel()

    def setup_main_panel(self):
        """
        Called at initialization.
        """
        self.toolbar = CustomToolBar(self)
        self.main_layout.insertWidget(0, self.toolbar)
        self.table = TasksTab(self, tab_columns)
        self.central_layout.addWidget(self.table)

    def setup_task_panel(self, task):
        """
        Called at click on table.
        """
        if not hasattr(self, "task_panel"):
            self.table.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)

            self.task_panel = TaskPanel(self, task)

            self.central_layout.addWidget(self.task_panel)
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
