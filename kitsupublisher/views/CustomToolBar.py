from Qt import QtCore, QtGui, QtWidgets

from kitsupublisher.utils.connection import open_browser
from kitsupublisher.utils.file import (
    get_icon_file,
    load_ui_file,
    get_pixmap_file,
    get_gif_file,
)


class CustomToolBar(QtWidgets.QWidget):

    def __init__(self, window):
        QtWidgets.QWidget.__init__(self)
        self.window = window
        self.setup_ui()

    def setup_ui(self):
        load_ui_file("ToolBarWidget.ui", self)

        self.logo_layout = self.findChild(QtWidgets.QLayout, "logo_layout")
        self.reload_btn = self.findChild(QtWidgets.QPushButton, "reload_btn")
        self.browser_btn = self.findChild(QtWidgets.QPushButton, "browser_btn")
        self.gif_label = self.findChild(QtWidgets.QLabel, "gif_label")

        self.setup_toolbar()
        self.paint_background()

    def setup_toolbar(self):
        self.reload_btn.setIcon(get_icon_file("refresh.png"))
        self.reload_btn.setIconSize(QtCore.QSize(25, 25))
        self.reload_btn.clicked.connect(self.window.reload)

        self.browser_btn.setIcon(get_icon_file("open-in-browser.png"))
        self.browser_btn.setIconSize(QtCore.QSize(25, 25))
        self.browser_btn.clicked.connect(open_browser)

        self.gif_file = get_gif_file("loading.gif")
        self.gif_label.setMovie(self.gif_file)
        self.gif_file.setScaledSize(QtCore.QSize(40, 40))
        self.show_loading_gif()

        pixmap = QtGui.QPixmap(get_pixmap_file("logo_kitsu.png"))
        pixmap = pixmap.scaled(40, 40, QtCore.Qt.KeepAspectRatio)
        self.label = QtWidgets.QLabel()
        self.label.setPixmap(pixmap)
        self.logo_layout.addWidget(self.label)
        self.title = QtWidgets.QLabel("My Kitsu Tasks")
        self.title.setFont(QtGui.QFont("Lato-Regular", 14))
        self.title.setStyleSheet("margin-left: 10px; font-weight: bold;")
        self.logo_layout.addWidget(self.title)

    def paint_background(self):
        pal = self.palette()
        pal.setColor(QtGui.QPalette.Background, QtGui.QColor("#292b2f"))
        self.setAutoFillBackground(True)
        self.setPalette(pal)

    def show_loading_gif(self):
        self.gif_file.start()
        self.gif_label.show()

    def hide_loading_gif(self):
        self.gif_file.stop()
        self.gif_label.hide()
