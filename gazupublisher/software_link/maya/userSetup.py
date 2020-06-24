import sys
import imp
import os

import maya.cmds as mc
import maya.mel
import maya.utils

gazupublisher_folder = ""
kitsu_host = ""

def launch_path_error_window(message=None):
    """
    Launch Maya dialog window
    """
    mc.confirmDialog(
        title="Error", message=message, button=["Ok"], defaultButton="Ok", cancelButton="Ok"
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


def launch_kitsu(*args):
    """
    Launch the publisher.
    """
    try:
        add_gazu_publisher_location_to_sys_path()
        import gazupublisher.__main__
        from gazupublisher.utils.connection import configure_host

        if kitsu_host:
            configure_host(kitsu_host)
        gazupublisher.__main__.main()
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
    menu = mc.menu("CGWire", parent=maya_window)
    mc.menuItem(label="Launch Kitsu", command=launch_kitsu, parent=menu)


maya.utils.executeDeferred(create_menu)
