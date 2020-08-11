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
