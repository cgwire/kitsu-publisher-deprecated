import os
import importlib

import Qt.QtWidgets as QtWidgets
import Qt.QtGui as QtGui
import Qt.QtCore as QtCore

from kitsupublisher.utils.file import load_ui_file
from kitsupublisher.utils.widgets import AnimatedLabel
from kitsupublisher.exceptions import (
    MediaNotSetUp,
    InvalidNodeError,
    RenderCameraError,
    OutputPathError,
    ContextNotFoundError
)
from kitsupublisher.views.task_panel.NoPreviewWidget import NoPreviewWidget
from kitsupublisher.working_context import (
    get_current_binding,
    is_blender_context,
    is_maya_context,
    is_houdini_context,
    is_nodal_context,
)

try:
    QtMultimedia = importlib.import_module(
        get_current_binding() + ".QtMultimedia"
    )
    QtMultimediaWidgets = importlib.import_module(
        get_current_binding() + ".QtMultimediaWidgets"
    )
except:
    pass


class TakePreviewWindow(QtWidgets.QDialog):
    """
    A window allowing the user to take previews directly from his software.
    """

    def __init__(self, comment_widget, is_video=False):
        super(TakePreviewWindow, self).__init__(comment_widget.panel.parent)
        self.comment_widget = comment_widget
        self.is_video = is_video
        self.setWindowTitle("Take preview")
        self.setModal(True)

        self.init_context()
        self.setup_ui()

        self.fill_camera_combobox()
        self.fill_extension_combobox()
        self.fill_renderer_combobox()
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
        self.renderer_widget = self.findChild(
            QtWidgets.QWidget, "renderer_widget"
        )
        self.renderer_cb = self.findChild(QtWidgets.QComboBox, "renderer_cb")
        self.renderer_label = self.findChild(QtWidgets.QLabel, "renderer_label")
        if is_houdini_context():
            self.renderer_label.setText("Render node :")
        self.extension_combobox = self.findChild(
            QtWidgets.QComboBox, "extension_combobox"
        )
        self.take_btn = self.findChild(QtWidgets.QPushButton, "take_btn")
        self.confirm_btn = self.findChild(QtWidgets.QPushButton, "confirm_btn")
        self.browse_btn = self.findChild(QtWidgets.QPushButton, "browse_btn")
        self.output_dir_line_edit = self.findChild(
            QtWidgets.QLineEdit, "output_dir_line_edit"
        )
        self.preview_widget = self.findChild(QtWidgets.QLabel, "preview_widget")
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

        self.form_widget = self.findChild(QtWidgets.QWidget, "form_widget")
        self.error_label = AnimatedLabel()
        self.form_widget.layout().insertWidget(5, self.error_label)
        self.error_label.hide()

    def init_context(self):
        """
        Initialize the context class, depending on which software is used.
        """
        if is_blender_context():
            from dccutils.blender import BlenderContext as Context
        elif is_maya_context():
            from dccutils.maya import MayaContext as Context
        elif is_houdini_context():
            from dccutils.houdini import HoudiniContext as Context
        else:
            raise ContextNotFoundError
        self.context = Context()

    def fill_camera_combobox(self):
        """
        Fill the combobox with all the available cameras.
        """
        cameras = self.context.list_cameras()
        for camera in cameras:
            name, camera_object = camera
            self.camera_combobox.addItem(name, userData=camera_object)

    def fill_extension_combobox(self):
        """
        Fill the combobox with the available extensions.
        Each extension is associated to an ID to identify its compression algorithm
        """
        list_extension = self.context.list_extensions(self.is_video)
        for ext_name, ext_id in list_extension:
            self.extension_combobox.addItem(ext_name, userData=ext_id)

    def fill_renderer_combobox(self):
        """
        Fill the combobox with the available renderers/render nodes.
        """
        list_renderers = self.context.get_available_renderers()
        if list_renderers:
            for renderer_name, renderer_data in list_renderers:
                self.renderer_cb.addItem(renderer_name, userData=renderer_data)

    def fill_output_dir(self, path=None):
        if not path:
            path = "/tmp/"
            if not os.path.isdir(path):
                path = ""
        self.output_dir_line_edit.setText(path)

    def fill_output_filename(self):
        self.filename_lineedit.setText("default")

    def fill_view_transform(self):
        """
        If a color space is detected, enable the option.
        """
        color_space = self.context.get_current_color_space()
        if color_space:
            self.viewtransform_label.setText(
                "Use current view transform (%s)" % (color_space)
            )
        else:
            self.viewtransform_label.hide()
            self.viewtransform_checkbox.hide()

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
        self.renderer_widget.setEnabled(True)

    def on_check_viewport(self):
        self.camera_widget.setEnabled(False)
        self.renderer_widget.setEnabled(False)

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

    def set_render_camera(self):
        """
        Set the selected camera as the rendering camera.
        The render node variable is not necessarily used, depending on the
        context.
        """
        camera = self.camera_combobox.currentData()
        renderer = self.renderer_cb.currentData()
        if is_nodal_context():
            if not self.context.check_node(renderer):
                self.show_error_label("Invalid node")
                raise InvalidNodeError()
        self.context.set_camera(camera, render_node=renderer)
        try:
            self.context.set_camera(camera, render_node=renderer)
        except:
            self.show_error_label(
                "Please select a camera. If none is available, "
                "Kitsu didn't find any in your scene"
            )
            raise RenderCameraError()

    def setup_preview_take(self):
        """
        Check arguments and save software current state.
        """
        try:
            output_path, extension_data = self.build_output_path()
            self.error_label.hide()
        except:
            raise OutputPathError()
        self.context.push_state()
        return output_path, extension_data

    def end_preview_take(self):
        """
        Set back software state.
        """
        self.context.pop_state()
        if is_houdini_context():
            self.show()
            self.activateWindow()

    def take_screenshot(self):
        """
        Take a screenshot and save it at the given path.
        """
        try:
            output_path, extension_data = self.setup_preview_take()
        except:
            return

        try:
            if self.viewport_checkbox.isChecked():
                self.context.take_viewport_screenshot(
                    output_path, extension_data
                )
            else:
                assert self.render_checkbox.isChecked()
                self.set_render_camera()
                self.error_label.hide()
                use_colorspace = self.viewtransform_checkbox.isChecked()
                renderer = self.renderer_cb.currentData()
                try:
                    self.context.take_render_screenshot(
                        renderer, output_path, extension_data, use_colorspace
                    )
                    # For some reason, arnold add "_1" to the output file name
                    if renderer == "arnold":
                        sep = os.path.splitext(output_path)
                        output_path = sep[0] + "_1" + sep[1]
                except Exception as e:
                    self.show_error_label(str(e))
                    return
        except:
            self.end_preview_take()
            return

        self.display_image_preview(output_path)
        self.set_output_path(output_path)
        self.update_confirm_btn()
        self.end_preview_take()

    def take_animation(self):
        try:
            output_path, extension_data = self.setup_preview_take()
        except:
            return

        try:
            if self.viewport_checkbox.isChecked():
                self.context.take_viewport_animation(
                    output_path, extension_data
                )
            else:
                assert self.render_checkbox.isChecked()
                self.set_render_camera()
                self.error_label.hide()
                use_colorspace = self.viewtransform_checkbox.isChecked()
                renderer = self.renderer_cb.currentData()
                try:
                    self.context.take_render_animation(
                        renderer, output_path, extension_data, use_colorspace
                    )
                except Exception as e:
                    self.show_error_label(str(e))
                    return
        except:
            self.end_preview_take()
            return

        try:
            self.display_video_preview(output_path)
        except:
            self.display_error_preview(output_path)

        self.set_output_path(output_path)
        self.update_confirm_btn()
        self.context.pop_state()
        self.end_preview_take()

    def display_image_preview(self, image_path):
        """
        Display the image.
        """
        pixmap = QtGui.QPixmap(image_path)
        pixmap = pixmap.scaled(
            self.preview_widget.size(), QtCore.Qt.KeepAspectRatio
        )
        self.preview_widget.setPixmap(pixmap)

    def display_video_preview(self, animation_path):
        """
        Display the video.
        """
        if is_blender_context() or is_maya_context() or is_houdini_context():
            raise MediaNotSetUp()

        self.clear_preview()

        self.preview_widget = QtMultimediaWidgets.QVideoWidget()
        self.preview_widget.resize(300, 300)
        self.preview_widget.move(0, 0)
        self.player = QtMultimedia.QMediaPlayer()
        self.player.setVideoOutput(self.preview_widget)
        self.player.setMedia(
            QtMultimedia.QMediaContent(
                QtCore.QUrl.fromLocalFile(animation_path)
            )
        )
        self.frame_preview_layout.addWidget(self.preview_widget)
        self.player.play()

    def display_error_preview(self, animation_path):
        """
        Display a replacement widget when previews couldn't be loaded.
        """
        self.clear_preview()
        message = (
            "Video lecture is not supported yet. <br/> "
            "If you want to look at it, the video is available by clicking the link below <br/>"
            "You can still select the file by hitting 'Confirm'"
        )
        folder_path = "file://" + os.path.dirname(animation_path)
        self.preview_widget = NoPreviewWidget(self, message, folder_path)
        self.frame_preview_layout.addWidget(self.preview_widget)

    def accept_preview(self):
        """
        Close the window and gives back to the comment widget the path of the
        capture.
        """
        if self.output_path:
            self.comment_widget.post_path = self.output_path
            self.comment_widget.update_selector_btn()
            self.accept()

    def clear_preview(self):
        if self.preview_widget:
            self.preview_widget.deleteLater()

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
