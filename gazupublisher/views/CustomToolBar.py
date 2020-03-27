from Qt import QtCore, QtGui, QtWidgets


import gazupublisher.utils.data as utils_data


class CustomToolBar(QtWidgets.QToolBar):

    def __init__(self, window):
        QtWidgets.QToolBar.__init__(self)
        self.window = window
        self.setupUi()

    def setupUi(self):
        self.combobox = QtWidgets.QComboBox()
        self.sort_attributes = {
            "Name": "entity_name",
            # "Priority": "priority",
            "Status": "task_status_short_name",
            "Estimation": "task_estimation",
            "Last comment": "last_comment"
        }
        self.combobox.insertItems(0, self.sort_attributes.keys())
        self.combobox.currentIndexChanged.connect(self.click_combobox)
        self.addWidget(self.combobox)

        self.reload_action = QtWidgets.QAction(QtGui.QIcon("../resources/icons/refresh.ico"), "reload_table", self)
        self.addAction(self.reload_action)
        self.actionTriggered[QtWidgets.QAction].connect(self.window.table.reload)

    def click_combobox(self):
        current_sort = self.combobox.currentText()
        sort_attribute = self.sort_attributes[current_sort]
        self.window.table.sort(sort_attribute)
