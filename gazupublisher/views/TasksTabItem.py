import Qt.QtWidgets as QtWidgets


class TasksTabItem(QtWidgets.QTableWidgetItem):
    def __init__(self, task, row, col, *args, **kwargs):
        QtWidgets.QTableWidgetItem.__init__(self, *args, **kwargs)
        self.task = task
        self.row = row
        self.col = col
