import sys
import gazu

import Qt.QtWidgets as QtWidgets


class CommentWindow(QtWidgets.QWidget):
    """
    A window that pops up when the user wants to enter a comment
    """
    def __init__(self, task, container):

        super().__init__()

        self.task = task
        self.container = container
        self.initUI()

    def initUI(self):
        self.btn = QtWidgets.QPushButton('Send', self)
        self.btn.move(105, 122.5)
        self.btn.clicked.connect(self.sendComment)

        self.le = QtWidgets.QTextEdit(self)
        self.le.setFixedSize(290, 120)
        # self.le.move(130, 22)

        self.setGeometry(300, 300, 290, 150)
        self.setWindowTitle('Comment')
        self.show()

    def sendComment(self):
        """
        Send the comment and reload all the tasks
        """
        text = self.le.document().toPlainText()

        if text:
            gazu.task.add_comment(self.task, self.task["task_status_id"], text)
            self.container.reload()

