import hou
import sys
import os
import imp

kitsupublisher_folder = ""


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
    Add the given path (supposed to contain the kitsu publisher) to sys.path
    """
    if not kitsupublisher_folder:
        message = "The location of the kitsu publisher module is not set.\nPlease set it and restart Houdini"
        launch_path_error_window(message)
        return

    path_kitsupublisher = os.path.normpath(kitsupublisher_folder)
    if path_kitsupublisher not in sys.path:
        sys.path.append(path_kitsupublisher)

    try:
        imp.find_module("kitsupublisher")
    except ImportError:
        message = (
                "The kitsu publisher module (expected at emplacement "
                + str(path_kitsupublisher)
                + ") was not found."
        )
        launch_path_error_window(message)
        raise


def launch_kitsu():
    """
    Launch the publisher.
    You can copy paste this function in a Houdini shelf and call it, to easily
    launch the interface.
    """
    try:
        import kitsupublisher.__main__
        from kitsupublisher.utils.connection import configure_host

        kitsu_host = os.environ.get("CGWIRE_HOST", None)
        if kitsu_host:
            configure_host(kitsu_host)
        kitsupublisher.__main__.main()
    except Exception as exc:
        print("Failed to launch Kitsu : %s" % exc)
        pass


add_gazu_publisher_location_to_sys_path()
