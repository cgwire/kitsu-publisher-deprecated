from Qt import QtCore, QtGui, QtWidgets, QtCompat

from gazupublisher.utils.data import get_all_previews_for_task
from gazupublisher.utils.other import is_video
from gazupublisher.utils.date import compare_date
from gazupublisher.views.task_panel.PreviewImageWidget import PreviewImageWidget
from gazupublisher.views.task_panel.PreviewVideoWidget import PreviewVideoWidget
from gazupublisher.views.task_panel.NoPreviewWidget import NoPreviewWidget
from gazupublisher.views.task_panel.ListCommentTask import ListCommentTask
from gazupublisher.views.task_panel.CommentWidget import CommentWidget


class TaskPanel(QtWidgets.QWidget):
    def __init__(self, parent, task):
        QtWidgets.QWidget.__init__(self, parent)
        self.parent = parent
        self.update_datas(task)

        self.setup_ui()
        self.desired_geometry = self.geometry()
        self.list_comments = ListCommentTask(self, self.task)
        self.post_comment_widget = CommentWidget(self, self.task)
        self.fill_widgets()
        self.add_widgets()

    def setup_ui(self):
        QtCompat.loadUi("../resources/views/TaskPanel.ui", self)
        self.scroll_area = self.findChild(QtWidgets.QScrollArea)
        self.scroll_widget = self.findChild(
            QtWidgets.QWidget, "scrollAreaWidgetContents"
        )
        self.scroll_area.setStyleSheet("QScrollBar {width:0px;}")

    def set_task(self, task):
        self.task = task

    def set_preview(self):
        """
        Set the preview file associated to the task. If not found, take the
        first one.
        """
        self.preview_file = None
        previews = get_all_previews_for_task(self.task)
        most_recent_preview_file = {"updated_at": "1900-01-01T00:00:00"}
        for preview in previews:
            if compare_date(preview["updated_at"], most_recent_preview_file["updated_at"]):
                most_recent_preview_file = preview
        if previews:
            self.preview_file = most_recent_preview_file

    def fill_widgets(self):
        """
        Fill the widgets with the datas.
        """
        self.fill_comments()
        self.update_post_comment_widget()
        self.create_preview()

    def add_widgets(self):
        """
        Add the widgets to the layout.
        """
        self.task_panel_vertical_layout.addWidget(self.preview_widget)
        self.task_panel_vertical_layout.addWidget(self.post_comment_widget)
        self.task_panel_vertical_layout.addWidget(self.list_comments)

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

    def update_post_comment_widget(self):
        """
        Update the task associated to the post comment widget.
        """
        self.post_comment_widget.set_task(self.task)

    def create_preview(self):
        """
        Create the preview following the type of object to display.
        """
        if not self.preview_file:
            self.preview_widget = NoPreviewWidget()

        else:
            if is_video(self.preview_file):
                self.preview_widget = PreviewVideoWidget(
                    self, self.preview_file
                )
            else:
                self.preview_widget = PreviewImageWidget(
                    self, self.preview_file
                )

    def reload(self):
        """
        Reload the widgets.
        """
        self.empty()
        self.update_datas(self.task)
        self.fill_widgets()
        self.add_widgets()
        self.scroll_area.verticalScrollBar().setValue(0)

    def empty(self):
        """
        Empty the comment widget and remove the preview widget.
        """
        self.list_comments.clear()
        self.preview_widget.clear()
        self.preview_widget.deleteLater()
        self.preview_widget = None
