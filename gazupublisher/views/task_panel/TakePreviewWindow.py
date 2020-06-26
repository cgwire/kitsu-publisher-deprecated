import os
import importlib

import Qt.QtWidgets as QtWidgets
import Qt.QtGui as QtGui
import Qt.QtCore as QtCore

from gazupublisher.working_context import get_current_binding

QtMultimedia = importlib.import_module(get_current_binding() + ".QtMultimedia")
QtMultimediaWidgets = importlib.import_module(
    get_current_binding() + ".QtMultimediaWidgets"
)

from gazupublisher.utils.file import load_ui_file
from gazupublisher.utils.widgets import AnimatedLabel
from gazupublisher.utils.software import (
    list_cameras,
    take_viewport_screenshot,
    take_render_screenshot,
    take_viewport_animation,
    take_render_animation,
    set_camera,
    get_current_color_space,
)


class TakePreviewWindow(QtWidgets.QDialog):
    """
    A window allowing the user to take previews directly from his software.
    """

    def __init__(self, comment_widget, is_video=False):
        super(QtWidgets.QDialog, self).__init__(comment_widget.panel.parent)
        self.comment_widget = comment_widget
        self.is_video = is_video
        self.setWindowTitle("Take preview")
        self.setModal(True)

        self.setup_ui()

        self.fill_camera_combobox()
        self.fill_extension_combobox()
        self.fill_output_dir()
        self.fill_output_filename()
        self.fill_view_transform()
        self.output_path = None

        if self.is_video:
            self.take_btn.clicked.connect(self.take_animation)
        else:
            self.take_btn.clicked.connect(self.take_screenshot)
        self.init_confirm_btn()
        self.browse_btn.clicked.connect(self.open_file_browser)
        self.render_checkbox.clicked.connect(self.on_check_render)
        self.viewport_checkbox.clicked.connect(self.on_check_viewport)
        self.viewport_checkbox.setChecked(True)
        self.on_check_viewport()
        self.viewtransform_checkbox.setChecked(True)

    def setup_ui(self):
        main_widget = QtWidgets.QWidget()
        load_ui_file("TakePreviewWidget.ui", main_widget)
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(main_widget)
        self.setLayout(layout)

        self.camera_widget = self.findChild(QtWidgets.QWidget, "camera_widget")
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
        self.render_checkbox = self.findChild(
            QtWidgets.QCheckBox, "render_checkbox"
        )
        self.viewport_checkbox = self.findChild(
            QtWidgets.QCheckBox, "viewport_checkbox"
        )
        self.viewtransform_checkbox = self.findChild(
            QtWidgets.QCheckBox, "viewtransform_checkbox"
        )
        self.viewtransform_label = self.findChild(
            QtWidgets.QLabel, "viewtransform_label"
        )
        self.frame_preview_layout = self.findChild(
            QtWidgets.QLayout, "frame_preview_layout"
        )
        self.preview_label = self.findChild(
            QtWidgets.QLabel, "preview_label"
        )

        self.form_widget = self.findChild(QtWidgets.QWidget, "form_widget")
        self.error_label = AnimatedLabel()
        self.form_widget.layout().insertWidget(4, self.error_label)
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
        if self.is_video:
            self.extension_combobox.addItem(".mp4", userData="MPEG4")
            self.extension_combobox.addItem(".mov", userData="QUICKTIME")
        else:
            self.extension_combobox.addItem(".png", userData="PNG")
            self.extension_combobox.addItem(".jpg", userData="JPEG")

    def fill_output_dir(self, path=None):
        if not path:
            path = "/tmp/"
        self.output_dir_line_edit.setText(path)

    def fill_output_filename(self):
        self.filename_lineedit.setText("default")

    def fill_view_transform(self):
        color_space = get_current_color_space()
        self.viewtransform_label.setText(
            "Use current view transform (%s)" % (color_space)
        )

    def init_confirm_btn(self):
        """
        Prevent confirmation without having generated preview
        """
        self.confirm_btn.setFlat(True)

    def update_confirm_btn(self):
        """
        Update confirm button after having generated preview
        """
        self.confirm_btn.clicked.connect(self.accept_preview)
        self.confirm_btn.setFlat(False)

    def open_file_browser(self):
        target_dir = QtWidgets.QFileDialog.getExistingDirectory(
            options=QtWidgets.QFileDialog.DontUseNativeDialog
        )
        self.fill_output_dir(target_dir)

    def on_check_render(self):
        self.camera_widget.setEnabled(True)

    def on_check_viewport(self):
        self.camera_widget.setEnabled(False)

    def build_output_path(self):
        """
        Build the path with the given input from the user
        :return: The valid path to store the image
        """
        dir = self.output_dir_line_edit.text()
        extension_data = self.extension_combobox.currentData()
        extension_txt = self.extension_combobox.currentText()
        filename = self.filename_lineedit.text()

        if not os.path.isdir(dir):
            self.show_error_label("Directory not found")
            raise FileNotFoundError
        if not filename:
            self.show_error_label("Please enter a filename")
            raise FileNotFoundError

        return os.path.join(dir, filename + extension_txt), extension_data

    def set_camera(self):
        """
        Set the selected camera as the rendering camera
        """
        camera = self.camera_combobox.currentData()
        try:
            set_camera(camera)
        except:
            self.show_error_label(
                "Please select a camera. If none is available, Kitsu didn't find any in your scene"
            )
            raise

    def take_screenshot(self):
        """
        Take a screenshot and save it at the given path.
        """
        try:
            output_path, extension = self.build_output_path()
            self.error_label.hide()
        except:
            return
        if self.viewport_checkbox.isChecked():
            take_viewport_screenshot(output_path, extension)
        else:
            assert self.render_checkbox.isChecked()
            try:
                self.set_camera()
            except:
                return
            use_viewtransform = self.viewtransform_checkbox.isChecked()
            take_render_screenshot(output_path, extension, use_viewtransform)
        self.display_image_preview(output_path)
        self.set_output_path(output_path)
        self.update_confirm_btn()

    def take_animation(self):
        try:
            output_path, container = self.build_output_path()
            self.error_label.hide()
        except:
            return
        if self.viewport_checkbox.isChecked():
            take_viewport_animation(output_path, container)
        else:
            assert self.render_checkbox.isChecked()
            try:
                self.set_camera()
            except:
                return
            use_viewtransform = self.viewtransform_checkbox.isChecked()
            take_render_animation(output_path, container, use_viewtransform)
        self.display_video_preview(output_path)
        self.set_output_path(output_path)
        self.update_confirm_btn()

    def display_image_preview(self, image_path):
        """
        Display the image.
        """
        pixmap = QtGui.QPixmap(image_path)
        pixmap = pixmap.scaled(
            self.preview_label.size(), QtCore.Qt.KeepAspectRatio
        )
        self.preview_label.setPixmap(pixmap)

    def display_video_preview(self, animation_path):
        """
        Display the video.
        """
        self.player = QtMultimedia.QMediaPlayer(self)

        self.playlist = QtMultimedia.QMediaPlaylist(self.player)
        self.content = QtMultimedia.QMediaContent(self.playlist, contentUrl=QtCore.QUrl(animation_path))
        self.playlist.addMedia(self.content)

        self.videoWidget = QtMultimediaWidgets.QVideoWidget()
        self.player.setVideoOutput(self.videoWidget)

        self.preview_label.deleteLater()
        self.frame_preview_layout.addWidget(self.videoWidget)

        self.player.play()

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

    def set_output_path(self, path):
        self.output_path = path

    def resizeEvent(self, event):
        if not self.is_video:
            self.display_image_preview(self.output_path)
        return super(QtWidgets.QDialog, self).resizeEvent(event)
