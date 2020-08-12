import os
from Qt import QtGui, QtCompat


def load_ui_file(ui_file, base_instance):
    current_abs_path = os.path.realpath(__file__)
    root_path = os.path.dirname(os.path.dirname(current_abs_path))
    ui_path = os.path.join(root_path, "resources", "views", ui_file)
    QtCompat.loadUi(ui_path, base_instance)


def load_translation_files(language_file_name):
    current_abs_path = os.path.realpath(__file__)
    root_path = os.path.dirname(os.path.dirname(current_abs_path))
    return os.path.join(
        root_path,
        "resources",
        "translations",
        "%s.qm" % language_file_name
    )


def get_icon_file(icon_file):
    current_abs_path = os.path.realpath(__file__)
    root_path = os.path.dirname(os.path.dirname(current_abs_path))
    icon_path = os.path.join(root_path, "resources", "images", "icons", icon_file)
    return QtGui.QIcon(icon_path)


def get_pixmap_file(pixmap_file):
    current_abs_path = os.path.realpath(__file__)
    root_path = os.path.dirname(os.path.dirname(current_abs_path))
    pixmap_path = os.path.join(root_path, "resources", "images", pixmap_file)
    return QtGui.QPixmap(pixmap_path)


def extract_filenames_list(list_paths):
    """
    Return a list of filenames from a list of paths.
    """
    return [os.path.basename(path) for path in list_paths]
