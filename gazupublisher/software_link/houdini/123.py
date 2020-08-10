import hou
import sys
import os
import imp

gazupublisher_folder = ""


def launch_path_error_window(message):
    """
    Launch Houdini error window
    """
    hou.ui.displayMessage(
        message,
        buttons=("OK",),
        severity=hou.severityType.Warning,
        title="Kitsu publisher error",
    )


def add_gazu_publisher_location_to_sys_path():
    """
    Add the given path (supposed to contain the gazu publisher) to sys.path
    """
    if not gazupublisher_folder:
        message = "The location of the gazu publisher module is not set.\nPlease set it and restart Maya"
        launch_path_error_window(message)
        return

    path_gazupublisher = os.path.normpath(gazupublisher_folder)
    if path_gazupublisher not in sys.path:
        sys.path.append(path_gazupublisher)

    try:
        imp.find_module("gazupublisher")
    except ImportError:
        message = (
                "The gazu publisher module (expected at emplacement "
                + str(path_gazupublisher)
                + ") was not found."
        )
        launch_path_error_window(message)
        raise


def launch_kitsu(kitsu_host=None, *args):
    """
    Launch the publisher.
    You can copy paste this function in a Houdini shelf and call it, to easily
    launch the interface.
    """
    try:
        import gazupublisher.__main__
        from gazupublisher.utils.connection import configure_host

        if kitsu_host:
            configure_host(kitsu_host)
        gazupublisher.__main__.main()
    except Exception as exc:
        print("Failed to launch Kitsu : %s" % exc)
        pass


add_gazu_publisher_location_to_sys_path()
