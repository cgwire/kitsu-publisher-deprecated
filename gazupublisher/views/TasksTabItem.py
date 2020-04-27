import Qt.QtWidgets as QtWidgets
import Qt.QtGui as QtGui
import Qt.QtCore as QtCore

from gazupublisher.utils.other import combine_colors
from gazupublisher.utils.date import format_table_date


class TasksTabItem(QtWidgets.QTableWidgetItem):
    def __init__(self, parent, row, col, task, task_attribute, *args, **kwargs):
        QtWidgets.QTableWidgetItem.__init__(self, *args, **kwargs)
        self.parent = parent
        self.row_nb = row
        self.col_nb = col
        self.task = task
        self.task_attribute = task_attribute

        self.set_text()
        self.is_bg_colored = False
        self.paint_background()
        self.paint_foreground()

    def set_text(self):
        """
        Set item text and change display depending on the current task attribute.
        """
        self.setTextAlignment(QtCore.Qt.AlignLeft)
        text = self.task[self.task_attribute]
        if isinstance(self.task[self.task_attribute], dict):
            assert self.task_attribute == "last_comment", (
                "Undefined behaviour, "
                "maybe following the "
                "addition of a new "
                "attribute ?"
            )
            if self.task[self.task_attribute]:
                text = self.task[self.task_attribute]["text"]

        else:
            if self.task_attribute == "task_due_date" and text:
                text = format_table_date(text)
            elif self.task_attribute == "entity_name":
                text = self.task["entity_type_name"] + "/" + text
            elif self.task_attribute == "task_status_short_name":
                text = text.upper()
            elif self.task_attribute == "task_duration":
                text = str(round(int(text)/(5*8*12), 1))
        self.setText(str(text))

    def paint_background(self):
        """
        Paint the current item with the appropriate background color.
        """
        color = self.background().color()
        if self.task_attribute == "task_type_name":
            color_task_type = QtGui.QColor(self.task["task_type_color"])
            color = combine_colors(color, color_task_type, factor=0.3)
            self.is_bg_colored = True
        elif (
            self.task_attribute == "task_status_short_name"
            or self.task_attribute == "task_status_name"
        ):
            color_task_status = QtGui.QColor(self.task["task_status_color"])
            color = combine_colors(color, color_task_status)
            self.is_bg_colored = True
        brush = QtGui.QBrush(color)
        self.setBackground(brush)

    def paint_foreground(self):
        """
        Paint the current item with the appropriate foreground color.
        """
        self.setForeground(QtGui.QBrush(QtGui.QColor(self.parent.text_color)))

    def __lt__(self, other):
        """
        Define the sorting of the items.
        Tasks are sorted by project names, then by types, and finally by names.
        """
        if self.task["project_name"] != other.task["project_name"]:
            return self.task["project_name"] < other.task["project_name"]
        if self.task["task_type_name"] != other.task["task_type_name"]:
            return self.task["task_type_name"] < other.task["task_type_name"]
        return (
            self.task["entity_type_name"] + self.task["entity_name"]
            < other.task["entity_type_name"] + other.task["entity_name"]
        )
