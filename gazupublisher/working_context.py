from Qt import __binding__

global working_context
working_context = ""


def get_current_binding():
    return __binding__


def is_maya_context():
    return working_context == "MAYA"


def is_blender_context():
    return working_context == "BLENDER"


def is_standalone_context():
    return working_context == "STANDALONE"
