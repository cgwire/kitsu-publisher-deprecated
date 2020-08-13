import sys
import imp
import os

import maya.cmds as mc
import maya.mel
import maya.utils

kitsupublisher_folder = ""
kitsu_host = os.environ.get("CGWIRE_HOST", None)


def launch_path_error_window(message=None):
    """
    Launch Maya dialog window
    """
    mc.confirmDialog(
        title="Error",
        message=message,
        button=["Ok"],
        defaultButton="Ok",
        cancelButton="Ok",
    )


def add_gazu_publisher_location_to_sys_path():
    """
    Add the given path (supposed to contain the kitsu publisher) to sys.path
    """
    if not kitsupublisher_folder:
        message = "The location of the kitsu publisher module is not set.\nPlease set it and restart Maya"
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


def launch_kitsu(*args):
    """
    Launch the publisher.
    """
    try:
        add_gazu_publisher_location_to_sys_path()
        import kitsupublisher.__main__
        from kitsupublisher.utils.connection import configure_host

        if kitsu_host:
            configure_host(kitsu_host)
        kitsupublisher.__main__.main()
    except Exception as exc:
        print("Failed to launch Kitsu : %s" % exc)
        pass


def get_maya_main_window():
    """
    Return maya main window
    """
    return maya.mel.eval("$tmpVar=$gMainWindow")


def create_menu(*args):
    """
    Add an item into the Maya interface.
    """
    maya_window = get_maya_main_window()
    menu = mc.menu("Kitsu", parent=maya_window)
    mc.menuItem(label="Launch Kitsu", command=launch_kitsu, parent=menu)


maya.utils.executeDeferred(create_menu)
