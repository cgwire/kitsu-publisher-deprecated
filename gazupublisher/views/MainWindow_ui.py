# -*- coding: utf-8 -*-
from gazupublisher import resources_rc  # needed to load assets

from Qt import QtCore, QtWidgets

from gazupublisher.views.TasksTab import TasksTab
from gazupublisher.views.CustomToolBar import CustomToolBar
import gazupublisher.config as config


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("window")

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")

        self.table = TasksTab(self, config.tab_columns)
        self.table.verticalHeader().sectionResized.connect(self.fitToTable)
        self.table.horizontalHeader().sectionResized.connect(self.fitToTable)
        self.table.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.table.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.table.show()

        self.toolbar = CustomToolBar(self)
        self.toolbar.show()
        self.verticalLayout.addWidget(self.toolbar)
        self.verticalLayout.addWidget(self.table)

        MainWindow.setCentralWidget(self.centralwidget)

        self.fitToTable()
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def fitToTable(self):
        self.table.setFixedSize(
            self.table.horizontalHeader().length() + self.table.verticalHeader().width(),
            self.table.verticalHeader().length() + self.table.horizontalHeader().height()
        )
