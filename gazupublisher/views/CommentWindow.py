import Qt.QtCore as QtCore
import Qt.QtWidgets as QtWidgets

import gazupublisher.utils.data as utils_data
import gazupublisher.utils.file as utils_file


class CommentWindow(QtWidgets.QDialog):
    """
    A window that pops up when the user wants to enter a comment
    """

    def __init__(self, task, container):
        super().__init__()
        self.setParent(None)

        self.task = task
        self.container = container
        # self.setWindowModality(QtCore.Qt.ApplicationModal)
        self.initUI()

    def initUI(self):
        # wid = QtWidgets.QWidget(self)
        # self.setWidget(wid)

        self.combobox = QtWidgets.QComboBox()
        self.combobox.setSizePolicy(QtWidgets.QSizePolicy.Minimum,
                                    QtWidgets.QSizePolicy.Minimum)
        self.dict_task_status = utils_data.get_task_status_names()
        self.combobox.insertItems(0, self.dict_task_status.keys())

        self.file_selector_btn = QtWidgets.QPushButton(
            QtCore.QCoreApplication.translate("Preview button", "Add preview"))
        self.file_selector_btn.setSizePolicy(QtWidgets.QSizePolicy.Fixed,
                                             QtWidgets.QSizePolicy.Fixed)
        self.file_selector_btn.clicked.connect(self.open_file_selector)
        self.file_selector = None

        self.comment_btn = QtWidgets.QPushButton(
            QtCore.QCoreApplication.translate("Comment button", "Comment"))
        self.comment_btn.setSizePolicy(QtWidgets.QSizePolicy.Expanding,
                                       QtWidgets.QSizePolicy.Expanding)
        self.comment_btn.clicked.connect(self.send_comment)

        hbox = QtWidgets.QHBoxLayout()
        hbox.addWidget(self.comment_btn)
        hbox.addWidget(self.file_selector_btn)
        hbox.addWidget(self.combobox)

        self.le = QtWidgets.QTextEdit(self)
        self.le.setSizePolicy(QtWidgets.QSizePolicy.Expanding,
                              QtWidgets.QSizePolicy.Expanding)

        vbox = QtWidgets.QVBoxLayout()
        vbox.addWidget(self.le)
        vbox.addLayout(hbox)

        self.setLayout(vbox)

        self.setGeometry(300, 300, 290, 150)
        self.setFixedSize(320, 170)
        self.setWindowTitle('Comment')

    def send_comment(self):
        """
        Send the comment and reload all the tasks
        """
        text = self.le.document().toPlainText()

        if text:
            wanted_task_status_short_name = self.dict_task_status[
                self.combobox.currentText()]
            task_status = utils_data.get_task_status_by_short_name(
                wanted_task_status_short_name)
            utils_data.post_comment(self.task, task_status, text)
            self.container.reload()
            self.container.window.fitToTable()
            self.accept()

    def open_file_selector(self):
        self.file_selector = QtWidgets.QFileDialog(
            options=QtWidgets.QFileDialog.DontUseNativeDialog)
        self.file_selector.setFileMode(QtWidgets.QFileDialog.ExistingFiles)
        # TODO Which formats do we authorize ?
        authorized_files = ["Images (*.png *.xpm *.jpg)",
                            "Video (*.mp4 *.avi *.raw)",
                            "Music (*.mp3, *.wav)",
                            "All (*)"]
        self.file_selector.setNameFilters(authorized_files)
        self.file_selector.setViewMode(QtWidgets.QFileDialog.Detail)
        # self.file_selector.setFocus()
        if self.file_selector.exec_():
            selected_files = self.file_selector.selectedFiles()
            self.update_selector_btn(selected_files)
            return selected_files
        # else:
        #     self.file_selector.show()
        #     self.file_selector.raise_()
        #     self.file_selector.activateWindow()

    def update_selector_btn(self, list_paths):
        list_files = utils_file.from_list_paths_to_list_files(list_paths)
        tooltip = str(list_files[0])
        for file in list_files[1:]:
            tooltip = tooltip + "\n" + file
        self.file_selector_btn.setToolTip(tooltip)
        # elidedText = metrics.elidedText(qText, Qt::ElideRight, textSnippet->width()-5)
        self.file_selector_btn.setText(tooltip)
