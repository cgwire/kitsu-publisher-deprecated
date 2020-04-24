import Qt.QtWidgets as QtWidgets
import Qt.QtGui as QtGui

from gazupublisher.ui_data.color import text_color


class NoPreviewWidget(QtWidgets.QWidget):
    """
    Widget to display when the task has no preview.
    """
    def __init__(self, *args, **kwargs):
        QtWidgets.QWidget.__init__(self, *args, **kwargs)
        self.no_preview_label = QtWidgets.QLabel("No preview yet")
        pal = self.no_preview_label.palette()
        pal.setColor(QtGui.QPalette.WindowText,
                     QtGui.QColor(text_color).darker(140))
        self.no_preview_label.setPalette(pal)
        self.no_preview_label.setFont(
            QtGui.QFont("Arial", pointSize=12, italic=True)
        )
        horizontal_label_layout = QtWidgets.QHBoxLayout(self)
        horizontal_label_layout.setSpacing(6)
        horizontal_label_layout.addWidget(self.no_preview_label)
        
    def clear(self):
        """
        Clear the children.
        """
        self.no_preview_label.deleteLater()
