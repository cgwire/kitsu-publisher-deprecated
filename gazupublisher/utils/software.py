"""
Module that act as an interface. Its purpose is to uniform the results coming
from different contexts.
"""


def take_screenshot(output_path, extension):
    """
    Take a screenshot
    """
    from gazupublisher.working_context import working_context

    if working_context == "BLENDER":
        from gazupublisher.utils.blender import take_screenshot

        take_screenshot(output_path, extension)
    elif working_context == "MAYA":
        from gazupublisher.utils.maya import take_screenshot

        take_screenshot(output_path, extension)


def list_cameras():
    """
    Return a list of tuple representing the cameras.
    Each tuple contains a camera object and its name.
    """
    import gazupublisher.working_context as w
    if w.working_context == "BLENDER":
        from gazupublisher.utils.blender import list_cameras

        return list_cameras()

    elif w.working_context == "MAYA":
        from gazupublisher.utils.maya import list_cameras

        return list_cameras()

    elif w.working_context == "STANDALONE":
        return [
            ("CameraStandAlone1", "CameraObject1"),
            ("CameraStandAlone2", "CameraObject2"),
        ]

def set_camera(camera):
    import gazupublisher.working_context as w

    if w.working_context == "BLENDER":
        from gazupublisher.utils.blender import set_camera

        set_camera(camera)
