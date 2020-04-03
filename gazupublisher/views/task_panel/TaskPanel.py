import os

from Qt import QtCore, QtGui, QtWidgets

from gazupublisher.utils.data import (
    get_all_comments_for_task,
    get_all_previews_for_task,
)
from gazupublisher.utils.connection import get_host
from gazupublisher.views.task_panel.PreviewImageWidget import PreviewImageWidget
from gazupublisher.views.task_panel.PreviewVideoWidget import PreviewVideoWidget
from gazupublisher.utils.format import is_video


class TaskPanel(QtWidgets.QWidget):
    def __init__(self, parent, task):
        QtWidgets.QWidget.__init__(self, parent)
        self.update_datas(task)
        self.horizontal_layout = QtWidgets.QHBoxLayout(self)
        self.list_comments = QtWidgets.QListWidget()
        self.fill_widgets()
        self.add_widgets()

    def update_datas(self, task):
        """
        Update the data.
        """
        self.set_task(task)
        self.set_preview()

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
        if not self.preview_file:
            self.preview_file = previews[0]

    def fill_widgets(self):
        """
        Fill the widgets with the datas.
        """
        self.fill_comments()
        self.create_preview()
        self.preview_widget.fill_preview()

    def add_widgets(self):
        """
        Add the widgets to the layout.
        """
        self.horizontal_layout.addWidget(self.preview_widget)
        self.horizontal_layout.addWidget(self.list_comments)

    def fill_comments(self):
        """
        Add the comments to the comment widget.
        """
        all_comments = get_all_comments_for_task(self.task)
        for comment in all_comments:
            text_comment = comment["text"]
            list_item = QtWidgets.QListWidgetItem(text_comment)
            self.list_comments.addItem(list_item)

    def create_preview(self):
        """
        Create the preview following the type of object to display.
        """
        if is_video(self.preview_file):
            url = os.path.join(
                get_host(),
                "movies",
                "originals",
                "preview-files",
                self.preview_file["id"] + "." + self.preview_file["extension"]
            )
            self.preview_widget = PreviewVideoWidget(url)
        else:
            url = os.path.join(
                get_host(),
                "pictures",
                "previews",
                "preview-files",
                self.preview_file["id"] + "." + self.preview_file["extension"]
            )
            self.preview_widget = PreviewImageWidget(url)

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
        self.horizontal_layout.removeWidget(self.preview_widget)
        self.preview_widget = None
