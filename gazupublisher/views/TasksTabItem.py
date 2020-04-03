import Qt.QtWidgets as QtWidgets


class TasksTabItem(QtWidgets.QTableWidgetItem):
    def __init__(self, task, *args, **kwargs):
        QtWidgets.QTableWidgetItem.__init__(self, *args, **kwargs)
        self.task = task
