"""
Module that act as a (loose)/us  interface. Its purpose is to uniform the results coming
from different contexts (Standalone, Blender, Maya, ...).
"""


class SoftwareContext:
    def __init__(self):
        self.output_path = None
        self.camera = None
        self.extension = None
        self.color_space = None

    def add_ui(self):
        pass

    def take_render_screenshot(self, output_path, extension, use_viewtransform=True):
        """
        Take a rendered screenshot
        """
        pass

    def take_viewport_screenshot(self, output_path, extension):
        """
        Take a viewport screenshot
        """
        pass

    def take_render_animation(
        self, output_path, container, use_viewtransform=True
    ):
        """
        Take a rendered animation
        """
        pass

    def take_viewport_animation(self, output_path, container):
        """
        Take a viewport animation
        """
        pass

    def push_state(self):
        """
        A function to save the current state (global variables) of the software.
        """
        pass

    def pop_state(self):
        """
        A function to set back the old state (global variables) of the software.
        """
        pass

    def list_cameras(self):
        """
        Return a list of tuple representing the cameras.
        Each tuple contains a camera object and its name.
        """
        pass

    def list_extensions(self, is_video):
        """
        Return a list of tuple representing the cameras.
        Each tuple contains a camera object and its name.
        """
        pass

    def get_current_color_space(self):
        pass

    def set_camera(self, camera):
        pass

    @staticmethod
    def software_print(data):
        pass
