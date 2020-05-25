import os

import Qt.QtCore as QtCore
import Qt.QtWidgets as QtWidgets
import Qt.QtGui as QtGui

import gazupublisher.utils.data as utils_data


class CommentWidget(QtWidgets.QWidget):
    """
    A widget for the user to enter a comment
    """

    def __init__(self, panel, task):
        super().__init__(panel)
        self.panel = panel
        self.task = task
        self.setFixedHeight(170)
        self.initUI()

    def initUI(self):

        self.combobox = QtWidgets.QComboBox()
        self.combobox.setSizePolicy(
            QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred
        )
        self.combobox.setFont(QtGui.QFont("Lato-Regular", 12))
        self.dict_task_status = utils_data.get_task_status_names()
        self.combobox.insertItems(0, self.dict_task_status.keys())

        self.file_selector_btn = QtWidgets.QPushButton(
            QtCore.QCoreApplication.translate("Preview button", "Add preview")
        )
        self.file_selector_btn.setSizePolicy(
            QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred
        )
        self.file_selector_btn.setFont(QtGui.QFont("Lato-Regular", 12))
        self.file_selector_btn.clicked.connect(self.open_file_selector)
        self.file_selector = None
        self.post_path = None

        self.comment_btn = QtWidgets.QPushButton(
            QtCore.QCoreApplication.translate("Comment button", "Comment")
        )
        self.comment_btn.setSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred
        )
        self.comment_btn.setFont(QtGui.QFont("Lato-Regular", 12))
        self.comment_btn.clicked.connect(self.send_comment_and_preview)

        hbox = QtWidgets.QHBoxLayout()
        hbox.addWidget(self.comment_btn)
        hbox.addWidget(self.file_selector_btn)
        hbox.addWidget(self.combobox)

        self.le = QtWidgets.QTextEdit(self)
        self.le.setSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding
        )
        self.le.setFont(QtGui.QFont("Lato-Regular", 12))
        self.le.setPlaceholderText("Comment")

        vbox = QtWidgets.QVBoxLayout()
        vbox.addWidget(self.le)
        vbox.addLayout(hbox)

        self.setLayout(vbox)

    def set_task(self, task):
        self.task = task

    def send_comment_and_preview(self):
        """
        Send the comment, the preview if it exists, and reload the app.
        """
        text = self.le.document().toPlainText()

        if text:
            wanted_task_status_short_name = self.dict_task_status[
                self.combobox.currentText()
            ]
            task_status = utils_data.get_task_status_by_short_name(
                wanted_task_status_short_name
            )
            comment = utils_data.post_comment(self.task, task_status, text)

            if self.post_path:
                utils_data.post_preview(self.task, comment, self.post_path)

            self.le.clear()
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

        font_metrics = QtGui.QFontMetrics(self.font())
        elided_text = font_metrics.elidedText(
            file_to_post,
            QtCore.Qt.ElideRight,
            self.file_selector_btn.width() - 5,
        )
        self.file_selector_btn.setFlat(True)
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

    def clear(self):
        """
        Clear the widget.
        """
        self.deleteLater()
