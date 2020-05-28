import Qt.QtWidgets as QtWidgets


class ResizableMessageBox(QtWidgets.QMessageBox):
    """
    Error window popping when an expected error happened.
    """
    def __init__(self, parent):
        QtWidgets.QMessageBox.__init__(self, parent)
        self.setSizeGripEnabled(True)

    def event(self, e):
        result = QtWidgets.QMessageBox.event(self, e)

        self.setMinimumHeight(100)
        self.setMaximumHeight(16777215)
        self.setMinimumWidth(200)
        self.setMaximumWidth(16777215)
        self.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)

        textEdit = self.findChild(QtWidgets.QTextEdit)
        if textEdit != None :
            textEdit.setMinimumHeight(400)
            textEdit.setMaximumHeight(16777215)
            textEdit.setMinimumWidth(800)
            textEdit.setMaximumWidth(16777215)
            textEdit.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)

        return result
