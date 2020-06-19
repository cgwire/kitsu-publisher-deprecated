import os

import Qt.QtCore as QtCore
import Qt.QtWidgets as QtWidgets
import Qt.QtGui as QtGui

import gazupublisher.utils.data as utils_data


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

        self.comment_text_edit = self.panel.findChild(QtWidgets.QTextEdit)
        self.comment_text_edit.setFont(QtGui.QFont("Lato-Regular", 12))
        self.comment_text_edit.setPlaceholderText("Comment")

        self.comment_btn.clicked.connect(self.send_comment_and_preview)
        self.file_selector_btn.clicked.connect(self.open_file_selector)

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

    def empty_text_edit(self):
        self.comment_text_edit.clear()

    def clear(self):
        """
        Clear the widget.
        """
        self.deleteLater()
