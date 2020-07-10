from Qt import QtCore, QtGui, QtWidgets

from gazupublisher.utils.connection import open_browser
from gazupublisher.utils.file import get_icon_file, load_ui_file, get_pixmap_file

class CustomToolBar(QtWidgets.QWidget):
    def __init__(self, window):
        QtWidgets.QWidget.__init__(self)
        self.window = window
        self.setupUi()

    def setupUi(self):
        load_ui_file("ToolBarWidget.ui", self)

        self.logo_layout = self.findChild(QtWidgets.QLayout, "logo_layout")
        self.reload_btn = self.findChild(QtWidgets.QPushButton, "reload_btn")
        self.browser_btn = self.findChild(QtWidgets.QPushButton, "browser_btn")

        self.setup_toolbar()

    def setup_toolbar(self):
        self.reload_btn.setIcon(get_icon_file("refresh.png"))
        self.reload_btn.setIconSize(QtCore.QSize(25, 25))
        self.reload_btn.clicked.connect(self.window.reload)
        self.browser_btn.setIcon(get_icon_file("open-in-browser.png"))
        self.browser_btn.setIconSize(QtCore.QSize(25, 25))
        self.browser_btn.clicked.connect(open_browser)

        pixmap = QtGui.QPixmap(get_pixmap_file("logo_cgwire.png"))
        pixmap = pixmap.scaled(144, 48, QtCore.Qt.KeepAspectRatio)
        self.label = QtWidgets.QLabel()
        self.label.setPixmap(pixmap)
        self.logo_layout.addWidget(self.label)

        pixmap = QtGui.QPixmap(get_pixmap_file("logo_kitsu.png"))
        pixmap = pixmap.scaled(40, 40, QtCore.Qt.KeepAspectRatio)
        self.label = QtWidgets.QLabel()
        self.label.setPixmap(pixmap)
        self.logo_layout.addWidget(self.label)

    def open_in_browser(self):
        open_browser()

    def click_combobox(self):
        self.window.table.activate_sort()

    def get_current_sort_attribute(self):
        current_sort = self.combobox.currentText()
        return self.dict_sort_attributes[current_sort]
