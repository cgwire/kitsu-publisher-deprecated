import Qt.QtWidgets as QtWidgets
import Qt.QtGui as QtGui
import Qt.QtCore as QtCore

from gazupublisher.ui_data.color import text_color


class NoPreviewWidget(QtWidgets.QWidget):
    """
    Widget displayed when the task has no preview.
    """

    def __init__(self, *args, **kwargs):
        QtWidgets.QWidget.__init__(self, *args, **kwargs)
        self.no_preview_label = QtWidgets.QLabel("No preview yet")
        pal = self.no_preview_label.palette()
        pal.setColor(
            QtGui.QPalette.WindowText, QtGui.QColor(text_color).darker(140)
        )
        self.no_preview_label.setPalette(pal)
        self.no_preview_label.setFont(
            QtGui.QFont("Arial", pointSize=12, italic=True)
        )

        horizontal_label_layout = QtWidgets.QHBoxLayout()
        horizontal_label_layout.setSpacing(0)
        horizontal_label_layout.addWidget(self.no_preview_label)
        self.setLayout(horizontal_label_layout)

        self.setSizePolicy(
            QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed
        )

    def clear(self):
        """
        Clear the children.
        """
        self.no_preview_label.deleteLater()

    def sizeHint(self):
        return QtCore.QSize(self.width(), 10)

    def get_height(self):
        return self.height()
