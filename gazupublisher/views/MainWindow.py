
import os
from Qt import QtCore, QtGui, QtWidgets

from .MainWindow_ui import Ui_MainWindow
from .. import exceptions

class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    """Main Window."""

    def __init__(self, app):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.app = app
        self.project_id = None  # TODO
        self.setupTranslation("ca_ES")
        self.setupUi(self)

    def setupTranslation(self, required_language=None):
        translator = QtCore.QTranslator()
        print("Local language : " + QtCore.QLocale.system().name())
        if required_language:
            path_file = "../resources/translations/" + required_language + ".qm"
            if translator.load(path_file):
                self.app.installTranslator(translator)
                print("Chosen language : " + required_language)
            else:
                raise exceptions.TranslationException("Loading of the translation file at path "
                                                      + os.path.abspath(path_file)
                                                      + " failed")
        else:
            path_file = "../resources/translations/" + QtCore.QLocale.system().name() + ".qm"
            translator.load(path_file)
            self.app.installTranslator(translator)
