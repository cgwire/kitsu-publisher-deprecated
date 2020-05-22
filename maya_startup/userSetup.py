import maya.cmds as mc
import maya.mel
import maya.utils

import subprocess

def get_maya_main_window():
    """
    Return maya main window
    """
    return maya.mel.eval("$tmpVar=$gMainWindow")


def launch_kitsu(*args):
    try:
        py_exec = "/usr/autodesk/maya2019/bin/mayapy"
        subprocess.call(
            [str(py_exec), "-m", "pip", "install", 
             "git+https://github.com/LedruRollin/gazu-publisher.git"], shell=True
        )
        subprocess.call(
            [str(py_exec), "-m", "pip", "freeze"], shell=True
        )
    except Exception as exc:
        print("Failed to install my_library: %s" % exc)
        pass
    print("TODO")


def create_menu(*args):

    maya_window = get_maya_main_window()
    #gMainFileMenu ?
    menu = mc.menu("TestFenetre", parent=maya_window)

    mc.menuItem(label="Launch Kitsu", command=launch_kitsu, parent=menu)
    return

maya.utils.executeDeferred(create_menu)
