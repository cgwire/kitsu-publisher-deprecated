import sys
import gazu
from gazupublisher.utils.data import get_task_status_names
import Qt.QtCore as QtCore

import Qt.QtWidgets as QtWidgets


class CommentWindow(QtWidgets.QMainWindow):
    """
    A window that pops up when the user wants to enter a comment
    """
    def __init__(self, task, container):

        super().__init__()
        self.setParent(None)

        self.task = task
        self.container = container
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        self.initUI()

    def initUI(self):
        wid = QtWidgets.QWidget(self)
        self.setCentralWidget(wid)

        self.cb = QtWidgets.QComboBox()
        self.dict_task_status = {"TODO":"todo", "WIP":"wip", "WFA":"wfa", "DONE":"done", "RETAKE":"retake"}
        self.cb.insertItems(0, list(self.dict_task_status.keys()))

        # app = self.container.window.app
        # self.login_btn = QtWidgets.QPushButton(app.translate("Comment", 'Send'), self)
        self.login_btn = QtWidgets.QPushButton(QtCore.QCoreApplication.translate("Comment button", "Comment"))
        self.login_btn.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self.login_btn.clicked.connect(self.sendComment)

        hbox = QtWidgets.QHBoxLayout()
        hbox.addWidget(self.login_btn)
        hbox.addWidget(self.combobox)

        self.le = QtWidgets.QTextEdit(self)
        self.le.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)

        vbox = QtWidgets.QVBoxLayout()
        vbox.addWidget(self.le)
        vbox.addLayout(hbox)

        wid.setLayout(vbox)

        self.setGeometry(300, 300, 290, 150)
        self.setFixedSize(320, 170)
        self.setWindowTitle('Comment')
        self.show()

    def sendComment(self):
        """
        Send the comment and reload all the tasks
        """
        text = self.le.document().toPlainText()

        if text:
            wanted_task_status_short_name = self.dict_task_status[self.cb.currentText()]
            task_status = gazu.task.get_task_status_by_short_name(wanted_task_status_short_name)
            gazu.task.add_comment(self.task, task_status, text)
            self.container.reload()
            self.container.window.fitToTable()
