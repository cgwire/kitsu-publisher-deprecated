import maya.cmds as mc
import maya.mel
import maya.utils


def launch_kitsu(*args):
    try:
        import gazupublisher.__main__

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
    maya_window = get_maya_main_window()
    # gMainFileMenu ?
    menu = mc.menu("CGWire", parent=maya_window)
    mc.menuItem(label="Launch Kitsu", command=launch_kitsu, parent=menu)

import sys
sys.path.append("/home/romain/.virtualenvs/maya_venv/lib/python2.7/site-packages")
maya.utils.executeDeferred(create_menu)
