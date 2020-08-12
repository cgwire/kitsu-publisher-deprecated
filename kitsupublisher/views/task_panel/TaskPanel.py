from Qt import QtCore, QtGui, QtWidgets, QtCompat

from kitsupublisher.utils.data import get_all_previews_for_task
from kitsupublisher.utils.format import is_video
from kitsupublisher.utils.date import compare_date
from kitsupublisher.utils.file import load_ui_file, get_icon_file
from kitsupublisher.utils.connection import get_host, open_task_in_browser
from kitsupublisher.utils.colors import combine_colors
from kitsupublisher.views.task_panel.PreviewImageWidget import PreviewImageWidget
from kitsupublisher.views.task_panel.NoPreviewWidget import NoPreviewWidget
from kitsupublisher.views.task_panel.ListCommentTask import ListCommentTask
from kitsupublisher.views.task_panel.CommentWidget import CommentWidget
from kitsupublisher.ui_data.color import main_color
from kitsupublisher.exceptions import MediaNotSetUp
from kitsupublisher.working_context import (
    is_blender_context,
    is_maya_context,
    is_houdini_context,
    get_current_binding,
)


class TaskPanel(QtWidgets.QWidget):
    """
    Panel containing task info, displayed after click on table row.
    """

    def __init__(self, parent, task):
        QtWidgets.QWidget.__init__(self)
        self.parent = parent
        self.update_datas(task)

        self.setup_ui()
        self.desired_geometry = self.geometry()
        self.init_widgets()
        self.create_widgets()
        self.add_widgets()

    def setup_ui(self):
        """
        Retrieve widgets from ui file.
        """
        load_ui_file("TaskPanel.ui", self)
        self.scroll_area = self.findChild(QtWidgets.QScrollArea)
        self.scroll_widget = self.findChild(
            QtWidgets.QWidget, "scrollAreaWidgetContents"
        )
        self.scroll_area.setStyleSheet("QScrollBar {width:0px;}")

        self.header_task = self.findChild(QtWidgets.QWidget, "header_task")
        self.header_task_entity_name = self.findChild(
            QtWidgets.QLabel, "header_task_entity_name"
        )
        self.header_task_type = self.findChild(
            QtWidgets.QLabel, "header_task_type"
        )
        self.header_task_open_webbrowser = self.findChild(
            QtWidgets.QPushButton, "header_task_open_webbrowser"
        )
        self.header_task_open_webbrowser.setText("")
        self.header_task_open_webbrowser.setIcon(
            get_icon_file("open-in-browser.png")
        )
        self.header_task_open_webbrowser.setToolTip("Open task in browser")

    def init_widgets(self):
        """
        Initialise the widgets.
        """
        self.post_comment_widget = CommentWidget(self, self.task)
        self.list_comments = None
        self.preview_widget = None

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
            if compare_date(
                preview["updated_at"], most_recent_preview_file["updated_at"]
            ):
                most_recent_preview_file = preview
        if previews:
            self.preview_file = most_recent_preview_file

    def set_url(self):
        if self.preview_file:
            self.kitsu_task_url = (
                get_host()[:-4]
                + "/productions/"
                + self.task["project_id"]
                + "/assets/tasks/"
                + self.task["id"]
                + "/previews/"
                + self.preview_file["id"]
            )

    def create_widgets(self):
        """
        Create the widgets.
        """
        self.update_header_labels()
        self.reload_post_comment_widget()
        self.create_preview()
        self.create_comments()

    def update_header_labels(self):
        """
        Update the task header by filling it with current task info.
        """
        self.update_header_task_type()
        self.update_header_task_name()
        self.update_header_button()

    def update_header_task_type(self):
        self.header_task_type.setText(self.task["task_type_name"])
        task_type_color = QtGui.QColor(self.task["task_type_color"])
        background_color = QtGui.QColor(main_color)
        mix_color = combine_colors(task_type_color, background_color)
        self.header_task_type.setStyleSheet(
            """QFrame{{ background: {0};border-radius: 4px;padding: 2px; }}""".format(
                mix_color.name()
            )
        )

    def update_header_task_name(self):
        self.header_task_entity_name.update()
        seq_name = self.task["sequence_name"]
        if seq_name:
            ep_name = self.task["episode_name"]
            if ep_name:
                full_entity_name = "{} / {} / {}".format(
                    ep_name, seq_name, self.task["entity_name"]
                )
            else:
                full_entity_name = "{} / {}".format(
                    seq_name, self.task["entity_name"]
                )
        else:
            full_entity_name = "{} / {}".format(
                self.task["entity_type_name"], self.task["entity_name"]
            )
        font_metrics = QtGui.QFontMetrics(self.header_task_entity_name.font())
        elided_text = font_metrics.elidedText(
            full_entity_name,
            QtCore.Qt.ElideRight,
            self.header_task_entity_name.width(),
        )
        self.header_task_entity_name.setToolTip(full_entity_name)
        self.header_task_entity_name.setText(elided_text)

    def update_header_button(self):
        signal = self.header_task_open_webbrowser.clicked
        receivers_count = self.header_task_open_webbrowser.receivers(
            str(signal)
            if get_current_binding().startswith("PySide")
            else signal
        )
        if receivers_count > 0:
            self.header_task_open_webbrowser.clicked.disconnect()
        self.header_task_open_webbrowser.clicked.connect(
            self.open_task_in_browser_
        )

    def open_task_in_browser_(self):
        return open_task_in_browser(self.task)

    def add_widgets(self):
        """
        Add the widgets to the layout.
        """
        self.task_panel_vertical_layout.insertWidget(1, self.preview_widget)
        self.task_panel_vertical_layout.addWidget(self.list_comments)

    def update_datas(self, task):
        """
        Update the data.
        """
        self.set_task(task)
        self.set_preview()
        self.set_url()

    def create_comments(self):
        """
        Create the list of comments widget.
        """
        self.list_comments = ListCommentTask(self, self.task)

    def reload_post_comment_widget(self):
        """
        Reload the post comment widget.
        """
        self.post_comment_widget.reload()

    def create_preview(self):
        """
        Create the preview following the type of object to display.
        """
        if not self.preview_file:
            self.preview_widget = NoPreviewWidget(self, "No preview yet")
        else:
            try:
                if is_video(self.preview_file):
                    if (
                        is_blender_context()
                        or is_maya_context()
                        or is_houdini_context()
                        or get_current_binding() not in ["PySide2", "PyQt5"]
                    ):
                        # Video not supported yet on Blender nor Maya
                        # Qt video support introduced in PySide2/PyQt5
                        raise MediaNotSetUp()
                    else:
                        from kitsupublisher.views.task_panel.PreviewVideoWidget import (
                            PreviewVideoWidget,
                        )

                        self.preview_widget = PreviewVideoWidget(
                            self, self.preview_file
                        )
                else:
                    self.preview_widget = PreviewImageWidget(
                        self, self.preview_file
                    )
            except MediaNotSetUp:
                self.preview_widget = None
                message = (
                    "Error while displaying the preview. <br/> Please "
                    "refer to the web interface by following this link :"
                )

                self.preview_widget = NoPreviewWidget(
                    self, message, self.kitsu_task_url
                )

    def reload(self):
        """
        Reload the widgets.
        """
        self.empty()
        self.update_datas(self.task)
        self.create_widgets()
        self.add_widgets()
        self.scroll_area.verticalScrollBar().setValue(0)

    def empty(self):
        """
        Empty the comment widget and remove the preview widget.
        """
        self.list_comments.empty()
        self.list_comments.deleteLater()
        self.list_comments = None
        self.preview_widget.clear()
        self.preview_widget.deleteLater()
        self.preview_widget = None
