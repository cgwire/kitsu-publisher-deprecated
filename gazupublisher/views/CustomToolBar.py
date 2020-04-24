from Qt import QtCore, QtGui, QtWidgets

from gazupublisher.utils.connection import open_browser
from gazupublisher.ui_data.color import main_color, text_color


class CustomToolBar(QtWidgets.QToolBar):
    def __init__(self, window):
        QtWidgets.QToolBar.__init__(self)
        self.window = window
        self.setStyleSheet(
            "QToolTip { color: "
            + text_color
            + "; "
            + "background-color: "
            + main_color
            + " ; border:0px; }"
        )
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

        self.reload_action = QtWidgets.QAction(
            QtGui.QIcon("../resources/icons/refresh.png"),
            "Reload the table",
            self,
        )
        self.reload_action.triggered.connect(self.window.reload)
        self.addAction(self.reload_action)

        self.open_in_browser_action = QtWidgets.QAction(
            QtGui.QIcon("../resources/icons/open-in-browser.png"),
            "Open in browser",
            self,
        )
        self.open_in_browser_action.triggered.connect(self.open_in_browser)
        self.addAction(self.open_in_browser_action)

    def open_in_browser(self):
        open_browser()

    def click_combobox(self):
        self.window.table.activate_sort()

    def get_current_sort_attribute(self):
        current_sort = self.combobox.currentText()
        return self.dict_sort_attributes[current_sort]
