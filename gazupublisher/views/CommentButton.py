import Qt.QtWidgets as QtWidgets


class CommentButton(QtWidgets.QPushButton):
    def __init__(self, comment_window, *args, **kwargs):
        QtWidgets.QCheckBox.__init__(self, *args, **kwargs)
        self.comment_window = comment_window
