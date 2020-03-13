import sys
import gazu
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

        self.login_btn = QtWidgets.QPushButton('Send', self)
        self.login_btn.clicked.connect(self.sendComment)

        hbox = QtWidgets.QHBoxLayout()
        hbox.addWidget(self.login_btn)
        hbox.addWidget(self.cb)
        hbox.addStretch(1)

        self.le = QtWidgets.QTextEdit(self)
        self.le.setFixedSize(290, 120)

        vbox = QtWidgets.QVBoxLayout()
        vbox.addWidget(self.le)
        vbox.addLayout(hbox)

        wid.setLayout(vbox)

        self.setGeometry(300, 300, 290, 150)
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

