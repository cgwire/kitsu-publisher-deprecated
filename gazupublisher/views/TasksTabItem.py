import Qt.QtWidgets as QtWidgets
import Qt.QtGui as QtGui

from gazupublisher.utils.other import combine_colors


class TasksTabItem(QtWidgets.QTableWidgetItem):
    def __init__(self, parent, row, col, task, task_attribute, *args, **kwargs):
        QtWidgets.QTableWidgetItem.__init__(self, *args, **kwargs)
        self.parent = parent
        self.row_nb = row
        self.col_nb = col
        self.task = task
        self.task_attribute = task_attribute
        self.paint_background()
        self.paint_foreground()

    def paint_background(self):
        """
        Paint the current item with the appropriate background color
        """
        color = (
            QtGui.QColor("#36393F")
            if self.row_nb % 2 == 0
            else QtGui.QColor("#46494f")
        )
        if self.task_attribute == "task_type_name":
            color_task_type = QtGui.QColor(self.task["task_type_color"])
            color = combine_colors(color, color_task_type)
        elif (
            self.task_attribute == "task_status_short_name"
            or self.task_attribute == "task_status_name"
        ):
            color_task_status = QtGui.QColor(self.task["task_status_color"])
            color = combine_colors(color, color_task_status)
        brush = QtGui.QBrush(color)
        self.setBackground(brush)

    def paint_foreground(self):
        """
        Paint the current item with the appropriate foreground color
        """
        self.setForeground(QtGui.QBrush(QtGui.QColor(self.parent.text_color)))