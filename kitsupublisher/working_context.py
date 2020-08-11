from Qt import __binding__

# By default the app is launched in standalone mode
working_context = "STANDALONE"


def get_current_binding():
    return __binding__


def set_working_context(context):
    global working_context
    working_context = context


def get_working_context():
    return working_context


def is_qt_context():
    """
    Return if the current context already relies on qt
    """
    return is_maya_context() or is_houdini_context()

def is_nodal_context():
    """
    Return if the current context is nodal
    """
    return is_houdini_context()


def is_maya_context():
    return working_context == "MAYA"


def is_blender_context():
    return working_context == "BLENDER"


def is_houdini_context():
    return working_context == "HOUDINI"


def is_standalone_context():
    return working_context == "STANDALONE"

