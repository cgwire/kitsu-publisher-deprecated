from Qt.QtWidgets import QMainWindow

from .MainWindow_ui import Ui_MainWindow


class MainWindow(QMainWindow, Ui_MainWindow):
    """Main Window."""

    def __init__(self):
        QMainWindow.__init__(self)
        self.project_id = None
        self.setupUi(self)
