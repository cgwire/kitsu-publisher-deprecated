import Qt.QtWidgets as QtWidgets
import Qt.QtGui as QtGui
import Qt.QtCore as QtCore

from kitsupublisher.ui_data.color import text_color


class NoPreviewWidget(QtWidgets.QWidget):
    """
    Widget displayed when the task has no preview.
    """

    def __init__(self, parent, message, url=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.parent = parent
        self.message = message
        self.preview_url = url
        self.no_preview_label = QtWidgets.QLabel(self.message)

        self.setup_color()

        if self.preview_url:
            self.setup_link()

        horizontal_label_layout = QtWidgets.QHBoxLayout()
        horizontal_label_layout.setContentsMargins(6, 6, 6, 6)
        horizontal_label_layout.addWidget(self.no_preview_label)
        self.setLayout(horizontal_label_layout)

        self.setSizePolicy(
            QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed
        )

    def setup_color(self):
        self.setStyleSheet('QLabel {color: %s}'%(QtGui.QColor(text_color).darker(140).name()))
        self.no_preview_label.setFont(
            QtGui.QFont("Arial", pointSize=12, italic=True)
        )

    def setup_link(self):
        self.no_preview_label.setText("<p> " + self.message + "</p>" +
                                      "<a href={}>Click Here</a>".format(self.preview_url))
        self.no_preview_label.setTextFormat(QtCore.Qt.RichText)
        self.no_preview_label.setOpenExternalLinks(True)
        self.no_preview_label.setTextInteractionFlags(QtCore.Qt.TextBrowserInteraction)

    def clear(self):
        """
        Clear the children.
        """
        self.no_preview_label.deleteLater()

    def sizeHint(self):
        return QtCore.QSize(self.width(), 40)

    def get_height(self):
        return self.height()
