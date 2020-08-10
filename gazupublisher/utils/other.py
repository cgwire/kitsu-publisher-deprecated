import Qt.QtGui as QtGui
import sys


def python_version():
    return sys.version_info


def check_module_import(module):
    """
    Return if given module is available
    """
    if python_version() < (3, 0):
        import imp
        try:
            imp.find_module(module)
            return True
        except ImportError:
            return False
    elif (3, 0) <= python_version() < (3, 4):
        import importlib
        spam_loader = importlib.find_loader(module)
        return spam_loader is not None
    else:
        assert (python_version() >= (3, 4))
        import importlib
        spam_spec = importlib.util.find_spec(module)
        return spam_spec is not None


def combine_colors(c1, c2, factor=0.5):
    """
    Return the mix color given two colors.
    """
    c3 = QtGui.QColor()
    c3.setRed(int((factor * c1.red() + (1 - factor) * c2.red())))
    c3.setGreen(int((factor * c1.green() + (1 - factor) * c2.green())))
    c3.setBlue(int((factor * c1.blue() + (1 - factor) * c2.blue())))
    return c3


def from_min_to_day(time):
    """
    Convert a str time with minutes as a unit (i.e. a task duration), into
    another str rounded time with an 8-hour day as a unit.
    """
    return str(round(int(time) / (60 * 8), 1))
