from Qt import QtCore, QtGui, QtWidgets, QtCompat

from gazupublisher.utils.data import get_all_previews_for_task
from gazupublisher.utils.other import is_video
from gazupublisher.views.task_panel.PreviewImageWidget import PreviewImageWidget
from gazupublisher.views.task_panel.PreviewVideoWidget import PreviewVideoWidget
from gazupublisher.views.task_panel.ListCommentTask import ListCommentTask


class TaskPanel(QtWidgets.QWidget):
    def __init__(self, parent, task):
        QtWidgets.QWidget.__init__(self, parent)
        self.update_datas(task)

        self.setup_ui()
        self.list_comments = ListCommentTask(self.task)
        self.fill_widgets()
        self.add_widgets()



    def setup_ui(self):
        a = QtCompat.loadUi("../resources/views/TaskPanel.ui", self)
        print(a)
        self.scrollArea = self.findChild(QtWidgets.QScrollArea)

    def set_task(self, task):
        self.task = task

    def set_preview(self):
        """
        Set the preview file associated to the task. If not found, take the
        first one.
        """
        self.preview_file = None
        previews = get_all_previews_for_task(self.task)
        for preview in previews:
            if preview["id"] == self.task["entity_preview_file_id"]:
                self.preview_file = preview
        if not self.preview_file and previews:
            self.preview_file = previews[0]

    def fill_widgets(self):
        """
        Fill the widgets with the datas.
        """
        self.fill_comments()
        self.create_preview()

    def add_widgets(self):
        """
        Add the widgets to the layout.
        """
        self.task_panel_vertical_layout.addWidget(self.preview_widget)
        self.task_panel_vertical_layout.addWidget(self.list_comments)

        for i in range(self.task_panel_vertical_layout.count()):
            widget = self.task_panel_vertical_layout.itemAt(i).widget()
            print(widget)

    def update_datas(self, task):
        """
        Update the data.
        """
        self.set_task(task)
        self.set_preview()
        if hasattr(self, "list_comments"):
            self.list_comments.set_task(task)

    def fill_comments(self):
        """
        Add the comments to the comment widget.
        """
        self.list_comments.fill_comments()

    def create_preview(self):
        """
        Create the preview following the type of object to display.
        """
        if not self.preview_file:
            self.preview_widget = QtWidgets.QLabel("No preview yet")
            self.preview_widget.setFont(
                QtGui.QFont("Arial", pointSize=10, italic=True)
            )
        else:
            if is_video(self.preview_file):
                self.preview_widget = PreviewVideoWidget(self, self.preview_file)
            else:
                self.preview_widget = PreviewImageWidget(self, self.preview_file)

    def reload(self):
        """
        Reload the widgets.
        """
        self.empty()
        self.fill_widgets()
        self.add_widgets()

    def empty(self):
        """
        Empty the comment widget and remove the preview widget.
        """
        self.list_comments.clear()
        self.preview_widget.clear()
