from Qt import QtCore, QtGui, QtWidgets


class CustomToolBar(QtWidgets.QToolBar):
    def __init__(self, window):
        QtWidgets.QToolBar.__init__(self)
        self.window = window
        self.setupUi()

    def setupUi(self):
        self.combobox = QtWidgets.QComboBox()
        self.dict_sort_attributes = {
            "Name": "entity_name",
            # "Priority": "priority",
            "Status": "task_status_short_name",
            "Estimation": "task_estimation",
            "Last comment": "last_comment",
        }
        self.combobox.insertItems(0, self.dict_sort_attributes.keys())
        self.combobox.currentIndexChanged.connect(self.click_combobox)
        self.addWidget(self.combobox)

        self.reload_action = QtWidgets.QAction(
            QtGui.QIcon("../resources/icons/refresh.ico"), "reload_table", self
        )
        self.addAction(self.reload_action)
        self.actionTriggered[QtWidgets.QAction].connect(
            self.window.table.reload
        )

    def click_combobox(self):
        sort_attribute = self.get_current_sort_attribute()
        self.window.table.sort()

    def get_current_sort_attribute(self):
        current_sort = self.combobox.currentText()
        return self.dict_sort_attributes[current_sort]
