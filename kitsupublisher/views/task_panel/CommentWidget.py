import os

import Qt.QtCore as QtCore
import Qt.QtWidgets as QtWidgets
import Qt.QtGui as QtGui

import kitsupublisher.utils.data as utils_data
from kitsupublisher.views.task_panel.TakePreviewWindow import TakePreviewWindow
from kitsupublisher.working_context import (
    is_standalone_context,
    is_houdini_context,
    is_maya_context,
    is_blender_context,
)


class NoScrollComboBox(QtWidgets.QComboBox):
    """
    QtWidgets.QComboBox holding available task status.
    """

    def __init__(self, parent, list_task_status):
        QtWidgets.QComboBox.__init__(self)
        self.parent = parent
        self.list_task_status = list_task_status
        self.setObjectName("task_status_combobox")
        self.add_items()
        self.select_most_recent_item()

        self.setFont(QtGui.QFont("Lato-Regular", 12))
        self.currentIndexChanged.connect(self.on_index_changed)

    def wheelEvent(self, *args, **kwargs):
        """
        Prevent parasite scrolling.
        """
        return self.parent.panel.wheelEvent(*args, **kwargs)

    def add_items(self):
        for row, task_status in enumerate(self.list_task_status):
            self.addItem(
                str(task_status["short_name"]).upper(), userData=task_status
            )
            color = QtGui.QColor(task_status["color"]).darker(180)
            self.model().item(row).setBackground(color)

    def select_most_recent_item(self):
        """
        The default task status is set as the one of the most recent comment, if
        it exists.
        """
        most_recent_comment = utils_data.get_last_comment_for_task(
            self.parent.task
        )
        if most_recent_comment:
            task_status = most_recent_comment["task_status"]
            task_status_short_name = task_status["short_name"].upper()
            for i in range(self.count()):
                current_short_name = self.model().item(i).data(0)
                if current_short_name == task_status_short_name:
                    self.setCurrentIndex(i)
                    return

    def change_background_color(self, color):
        pal = self.palette()
        pal.setColor(QtGui.QPalette.Button, QtGui.QColor(color).darker(200))
        self.setPalette(pal)

    def on_index_changed(self):
        color = self.currentData()["color"]
        self.change_background_color(color)
        self.parent.change_header_color(color)


class CommentWidget(QtWidgets.QWidget):
    """
    A widget for the user to enter a comment.
    """

    def __init__(self, panel, task):
        QtWidgets.QWidget.__init__(self, panel)
        self.panel = panel
        self.task = task
        self.setup_ui()

    def setup_ui(self):

        self.post_comment_header = self.panel.findChild(
            QtWidgets.QPushButton, "post_comment_header"
        )
        self.comment_btn = self.panel.findChild(
            QtWidgets.QPushButton, "comment_btn"
        )
        self.file_selector_btn = self.panel.findChild(
            QtWidgets.QPushButton, "file_selector_btn"
        )
        self.buttons_layout = self.panel.findChild(
            QtWidgets.QLayout, "buttons_layout"
        )

        self.dict_task_status = utils_data.get_accessible_task_status()
        self.combobox = NoScrollComboBox(self, self.dict_task_status)
        self.buttons_layout.addWidget(self.combobox)
        self.combobox.on_index_changed()

        self.post_path = None
        self.fill_preview_selector()

        self.comment_text_edit = self.panel.findChild(QtWidgets.QTextEdit)
        self.comment_text_edit.setFont(QtGui.QFont("Lato-Regular", 12))
        self.comment_text_edit.setPlaceholderText("Comment")

        self.comment_btn.clicked.connect(self.send_comment_and_preview)

        self.comment_shortcut = QtWidgets.QShortcut(
            QtGui.QKeySequence("Ctrl+Return"), self
        )
        self.comment_shortcut.activated.connect(self.send_comment_and_preview)

    def set_task(self, task):
        self.task = task

    def send_comment_and_preview(self):
        """
        Send the comment, the preview if it exists, and reload the app.
        """
        text = self.comment_text_edit.document().toPlainText()

        task_status = self.combobox.currentData()
        comment = utils_data.post_comment(self.task, task_status, text)

        if self.post_path:
            utils_data.post_preview(self.task, comment, self.post_path)

        self.comment_text_edit.clear()
        self.reset_selector_btn()
        self.panel.parent.reload()

    def get_preview_selector_items(self):
        """
        Return available previews depending on the context.
        """
        if is_maya_context() or is_blender_context():
            return ["Take screenshot", "Take playblast", "From local file"]
        elif is_houdini_context():
            return ["Take screenshot", "From local file"]
        else:
            return ["From local file"]

    def fill_preview_selector(self):
        """
        Fill the preview selector button.
        """
        menu = QtWidgets.QMenu(self.file_selector_btn)
        items = self.get_preview_selector_items()
        for s in items:
            menu.addAction(s)
        self.file_selector_btn.setMenu(menu)
        menu.triggered.connect(self.take_preview)

    def take_preview(self, action):
        if action.text() == "From local file":
            self.open_file_selector()
        else:
            if action.text() == "Take screenshot":
                preview_window = TakePreviewWindow(self)
            else:
                preview_window = TakePreviewWindow(self, is_video=True)
            preview_window.show()
            preview_window.raise_()
            preview_window.activateWindow()

    def open_file_selector(self):
        """
        Open the file selector.
        """
        self.file_selector = QtWidgets.QFileDialog(
            options=QtWidgets.QFileDialog.DontUseNativeDialog
        )
        self.file_selector.setFileMode(QtWidgets.QFileDialog.ExistingFile)
        authorized_files = [
            "All media files (*.png *.jpg *.jpeg *.mp4 *.mov *.wmv *.obj)",
            "Images (*.png *.jpg *.jpeg)",
            "Video (*.mp4 *.mov *.wmv)",
            "3D (*.obj)",
        ]
        self.file_selector.setNameFilters(authorized_files)
        self.file_selector.setViewMode(QtWidgets.QFileDialog.Detail)
        if self.file_selector.exec_():
            selected_file = self.file_selector.selectedFiles()
            self.post_path = selected_file[0]
            self.update_selector_btn()

    def update_selector_btn(self):
        """
        Update the button appearance following the selection by the user of the
        files to post.
        """
        file_to_post = os.path.basename(self.post_path)
        self.file_selector_btn.setToolTip(file_to_post)

        font_metrics = QtGui.QFontMetrics(self.file_selector_btn.font())
        elided_text = font_metrics.elidedText(
            file_to_post,
            QtCore.Qt.ElideRight,
            self.file_selector_btn.width() - 5,
        )
        self.file_selector_btn.setText(elided_text)

    def reset_selector_btn(self):
        """
        Reset the selector button appearance.
        """
        self.file_selector_btn.setToolTip("")
        self.file_selector_btn.setFlat(False)
        self.file_selector_btn.setText(
            QtCore.QCoreApplication.translate("Preview button", "Add preview")
        )

    def change_header_color(self, color_hex):
        self.post_comment_header.setEnabled(False)
        color = QtGui.QColor(color_hex)
        darker_color = color.darker(170)
        pal = self.post_comment_header.palette()
        pal.setColor(QtGui.QPalette.Button, darker_color)

        self.post_comment_header.setPalette(pal)
        self.post_comment_header.setAutoFillBackground(True)
        self.post_comment_header.update()

    def reload(self):
        self.empty_text_edit()
        self.reset_selector_btn()
        self.set_task(self.panel.task)
        self.combobox.select_most_recent_item()

    def empty_text_edit(self):
        self.comment_text_edit.clear()

    def clear(self):
        """
        Clear the widget.
        """
        self.deleteLater()
