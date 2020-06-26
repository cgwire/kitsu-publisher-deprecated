"""
Module that act as an interface. Its purpose is to uniform the results coming
from different contexts.
"""

from gazupublisher.working_context import (
    is_blender_context,
    is_maya_context,
    is_standalone_context,
)


def take_render_screenshot(output_path, extension, use_viewtransform=True):
    """
    Take a rendered screenshot
    """

    if is_blender_context():
        from gazupublisher.utils.blender import (
            take_render_screenshot,
            set_current_color_space,
        )

        if not use_viewtransform:
            set_current_color_space("Raw")
        take_render_screenshot(output_path, extension)
    elif is_maya_context():
        from gazupublisher.utils.maya import take_screenshot

        take_screenshot(output_path, extension)


def take_viewport_screenshot(output_path, extension):
    """
    Take a viewport screenshot
    """

    if is_blender_context():
        from gazupublisher.utils.blender import take_viewport_screenshot

        take_viewport_screenshot(output_path, extension)
    elif is_maya_context():
        from gazupublisher.utils.maya import take_screenshot

        take_screenshot(output_path, extension)


def take_render_animation(output_path, container, use_viewtransform=True):
    """
    Take a rendered animation
    """
    if is_blender_context():
        from gazupublisher.utils.blender import (
            take_render_animation,
            set_current_color_space,
        )

        if not use_viewtransform:
            set_current_color_space("Raw")
        take_render_animation(output_path, container)
    elif is_maya_context():
        from gazupublisher.utils.maya import take_screenshot

        take_screenshot(output_path, container)


def take_viewport_animation(output_path, container):
    """
    Take a viewport animation
    """

    if is_blender_context():
        from gazupublisher.utils.blender import take_viewport_animation

        take_viewport_animation(output_path, container)
    elif is_maya_context():
        from gazupublisher.utils.maya import take_screenshot

        take_screenshot(output_path, container)


def list_cameras():
    """
    Return a list of tuple representing the cameras.
    Each tuple contains a camera object and its name.
    """
    if is_blender_context():
        from gazupublisher.utils.blender import list_cameras

        return list_cameras()

    elif is_maya_context():
        from gazupublisher.utils.maya import list_cameras

        return list_cameras()

    elif is_standalone_context():
        return [
            ("CameraStandAlone1", "CameraObject1"),
            ("CameraStandAlone2", "CameraObject2"),
        ]


def get_current_color_space():
    if is_blender_context():
        from gazupublisher.utils.blender import get_current_color_space

        return get_current_color_space()


def set_camera(camera):
    if is_blender_context():
        from gazupublisher.utils.blender import set_camera

        set_camera(camera)

def software_print(data):
    if is_blender_context():
        from gazupublisher.utils.blender import blender_print
        blender_print(data)
