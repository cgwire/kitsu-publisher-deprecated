# -*- coding: utf-8 -*-
from gazupublisher import resources_rc  # needed to load assets

from Qt import QtCore, QtGui, QtWidgets

from gazupublisher.views.TasksTab import TasksTab
from gazupublisher.views.CustomToolBar import CustomToolBar
import gazupublisher.config as config

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("window")

        # MainWindow.resize(800, 600)
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
        # self.label_2 = QtWidgets.QLabel(self.centralwidget)
        # self.label_2.setSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.MinimumExpanding)
        # self.label_2.setText("Tasks :")
        # self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        # self.label_2.setObjectName("label_2")
        # self.verticalLayout.addWidget(self.label_2)
        self.verticalLayout.addWidget(self.toolbar)
        self.verticalLayout.addWidget(self.table)

        MainWindow.setCentralWidget(self.centralwidget)

        self.fitToTable()
        # self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    # def retranslateUi(self, MainWindow):
    #     _translate = QtCore.QCoreApplication.translate
    #     MainWindow.setWindowTitle(_translate("MainWindow", "To-do tasks"))

    # @QtCore.pyqtSlot()
    def fitToTable(self):
        x = self.table.verticalHeader().size().width()
        for i in range(self.table.columnCount()):
            x += self.table.columnWidth(i)

        y = self.table.horizontalHeader().size().height()
        for i in range(self.table.rowCount()):
            y += self.table.rowHeight(i)

        # y += self.toolbar.height()
        # y = self.centralwidget.frameGeometry().height()

        x = self.table.geometry().width()
        y = self.table.geometry().height()

        # self.setFixedSize(self.verticalLayout.sizeHint())
        # self.resize(self.sizeHint().width(), self.size().height());

        # self.setFixedSize(x+20, y+20)
        # self.setFixedSize(x, y)

        self.table.setFixedSize(self.table.horizontalHeader().length() +
                   self.table.verticalHeader().width(),
                   self.table.verticalHeader().length() +
                   self.table.horizontalHeader().height())