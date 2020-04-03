from Qt import QtWidgets, QtCompat


class PreviewWidget(QtWidgets.QWidget):
    def __init__(self, preview_file):
        super(PreviewWidget, self).__init__()
        self.preview_file = preview_file
        self.setup_ui()
        self.complete_ui()

    def setup_ui(self):
        QtCompat.loadUi("../resources/views/PreviewWidget.ui", self)
        self.toolbar_widget = self.findChild(QtWidgets.QWidget, "toolbar_widget")
        self.annote_button = self.findChild(QtWidgets.QPushButton, "annote_button")
        self.delete_button = self.findChild(QtWidgets.QPushButton, "delete_button")
        self.download_button = self.findChild(QtWidgets.QPushButton, "download_button")
        self.full_screen_button = self.findChild(QtWidgets.QPushButton, "full_screen_button")

    def complete_ui(self):
        pass

    def clear(self):
        self.layout().removeWidget(self.annote_button)
        self.layout().removeWidget(self.delete_button)
        self.layout().removeWidget(self.download_button)
        self.layout().removeWidget(self.full_screen_button)
        self.layout().removeWidget(self.toolbar_widget)
        self.clear_setup_media_widget()
        self.deleteLater()

    def clear_setup_media_widget(self):
        pass