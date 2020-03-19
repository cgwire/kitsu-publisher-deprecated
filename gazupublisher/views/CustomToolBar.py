from Qt import QtCore, QtGui, QtWidgets

import gazupublisher.utils.data as utils_data


class CustomToolBar(QtWidgets.QToolBar):
    """Main Window."""

    def __init__(self, window):
        QtWidgets.QToolBar.__init__(self)
        self.window = window
        self.setupUi()

    def setupUi(self):
        self.combobox = QtWidgets.QComboBox()
        self.combobox.insertItems(0, utils_data.get_all_open_project_names())
        # self.combobox.currentIndexChanged.connect() #TODO
        self.addWidget(self.combobox)

        self.reload_action = QtWidgets.QAction(QtGui.QIcon("../resources/icons/refresh.ico"), "reload_table", self)
        self.addAction(self.reload_action)
        self.actionTriggered[QtWidgets.QAction].connect(self.window.table.reload)
        # self.actionTriggered[QtWidgets.QAction].connect(self.reload)


