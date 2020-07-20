from Qt import __binding__

working_context = ""


def get_current_binding():
    return __binding__


def set_working_context(context):
    global working_context
    working_context = context


def get_working_context():
    return working_context


def is_maya_context():
    return working_context == "MAYA"


def is_blender_context():
    return working_context == "BLENDER"


def is_standalone_context():
    return working_context == "STANDALONE"

