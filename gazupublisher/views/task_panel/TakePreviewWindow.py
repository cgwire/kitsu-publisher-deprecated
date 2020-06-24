import os
import re

import Qt.QtWidgets as QtWidgets
import Qt.QtGui as QtGui
import Qt.QtCore as QtCore

from gazupublisher.utils.file import load_ui_file
from gazupublisher.utils.software import (
    list_cameras,
    take_screenshot,
    set_camera,
)


class AnimatedLabel(QtWidgets.QLabel):
    """
    QLabel with animated background color.
    Used to display errors.
    """

    def __init__(self):
        super(AnimatedLabel, self).__init__()
        self.setStyleSheet(
            """
            background-color: #CC4444;
            color: #F5F5F5;
            padding: 5px;
            """
        )
        self.setWordWrap(True)
        self.create_animation()

    def create_animation(self):
        """
        Create the animation of the color background.
        """
        color_begin = QtGui.QColor("#943434")
        color_end = QtGui.QColor("#CC4444")
        self.color_anim = QtCore.QPropertyAnimation(self, b"background_color")
        self.color_anim.setStartValue(color_begin)
        self.color_anim.setEndValue(color_end)
        self.color_anim.setDuration(400)

    def start_animation(self):
        """
        Start the animation of the color background.
        """
        self.color_anim.stop()
        self.color_anim.start()

    def get_back_color(self):
        """
        Get the background color.
        """
        return self.palette().color(QtGui.QPalette.Window)

    def set_back_color(self, color):
        """
        Set the given color as background color by parsing the style sheet.
        """
        style = self.styleSheet()
        pattern = "background-color:[^\n;]*"
        new = "background-color: %s" % color.name()
        style = re.sub(pattern, new, style, flags=re.MULTILINE)
        self.setStyleSheet(style)

    # Property to animate : the label background color
    background_color = QtCore.Property(
        QtGui.QColor, get_back_color, set_back_color
    )


class TakePreviewWindow(QtWidgets.QDialog):
    """
    A window allowing the user to take previews directly from his software.
    """

    def __init__(self, comment_widget, action):
        super(QtWidgets.QDialog, self).__init__(comment_widget.panel.parent)
        self.comment_widget = comment_widget
        self.action = action
        self.setWindowTitle("Take preview")
        self.setModal(True)

        self.setup_ui()

        self.fill_camera_combobox()
        self.fill_extension_combobox()
        self.fill_output_dir()
        self.fill_output_filename()
        self.output_path = None

        self.take_btn.clicked.connect(self.take_screenshot)
        self.init_confirm_btn()
        self.browse_btn.clicked.connect(self.open_file_browser)

    def setup_ui(self):
        main_widget = QtWidgets.QWidget()
        load_ui_file("TakePreviewWidget.ui", main_widget)
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(main_widget)
        self.setLayout(layout)

        self.camera_combobox = self.findChild(
            QtWidgets.QComboBox, "camera_combobox"
        )
        self.extension_combobox = self.findChild(
            QtWidgets.QComboBox, "extension_combobox"
        )
        self.take_btn = self.findChild(QtWidgets.QPushButton, "take_btn")
        self.confirm_btn = self.findChild(QtWidgets.QPushButton, "confirm_btn")
        self.browse_btn = self.findChild(QtWidgets.QPushButton, "browse_btn")
        self.output_dir_line_edit = self.findChild(
            QtWidgets.QLineEdit, "output_dir_line_edit"
        )
        self.preview_label = self.findChild(QtWidgets.QLabel, "preview_label")
        self.filename_lineedit = self.findChild(
            QtWidgets.QLineEdit, "filename_lineedit"
        )

        self.form_widget = self.findChild(QtWidgets.QWidget, "form_widget")
        self.error_label = AnimatedLabel()
        self.form_widget.layout().insertWidget(3, self.error_label)
        self.error_label.hide()

    def fill_camera_combobox(self):
        """
        Fill the combobox with all the available cameras
        """
        cameras = list_cameras()
        for camera in cameras:
            name, camera_object = camera
            self.camera_combobox.addItem(name, userData=camera_object)

    def fill_extension_combobox(self):
        """
        Fill the combobox with the available extensions.
        Each extension is associated to a compression algorithm for Blender
        """
        self.extension_combobox.addItem(".png", userData="PNG")
        self.extension_combobox.addItem(".jpg", userData="JPEG")

    def fill_output_dir(self, path=None):
        if not path:
            path = "/tmp/"
        self.output_dir_line_edit.setText(path)

    def fill_output_filename(self):
        self.filename_lineedit.setText("default")

    def init_confirm_btn(self):
        self.confirm_btn.setFlat(True)

    def update_confirm_btn(self):
        self.confirm_btn.clicked.connect(self.accept_preview)
        self.confirm_btn.setFlat(False)

    def open_file_browser(self):
        target_dir = QtWidgets.QFileDialog.getExistingDirectory(
            options=QtWidgets.QFileDialog.DontUseNativeDialog
        )
        self.fill_output_dir(target_dir)

    def build_output_path(self):
        """
        Build the path with the given input from the user
        :return: The valid path to store the image
        """
        dir = self.output_dir_line_edit.text()
        extension_blender = self.extension_combobox.currentData()
        extension_txt = self.extension_combobox.currentText()
        filename = self.filename_lineedit.text()

        if not os.path.isdir(dir):
            self.show_error_label("Directory not found")
            raise FileNotFoundError
        if not filename:
            self.show_error_label("Please enter a filename")
            raise FileNotFoundError

        return os.path.join(dir, filename + extension_txt), extension_blender

    def take_screenshot(self):
        """
        Take a screenshot with the given camera and save it at the given path.
        """
        camera = self.camera_combobox.currentData()
        try:
            set_camera(camera)
        except:
            self.show_error_label(
                "Please select a camera. If none is available, Kitsu didn't find any in your scene"
            )
            return
        try:
            output_path, extension = self.build_output_path()
            self.error_label.hide()
        except:
            return
        take_screenshot(output_path, extension)
        self.display_preview(output_path)
        self.output_path = output_path
        self.update_confirm_btn()

    def display_preview(self, image_path):
        """
        Display the image.
        """
        pixmap = QtGui.QPixmap(image_path)
        pixmap = pixmap.scaled(
            self.preview_label.size(), QtCore.Qt.KeepAspectRatio
        )
        self.preview_label.setPixmap(pixmap)

    def accept_preview(self):
        """
        Close the window and gives back to the comment widget the path of the
        capture
        """
        if self.output_path:
            self.comment_widget.post_path = self.output_path
            self.comment_widget.update_selector_btn()
            self.accept()

    def show_error_label(self, text):
        self.error_label.setText(text)
        self.error_label.show()
        self.error_label.start_animation()
