import os

from Qt import QtCore, QtWidgets

from .MainWindow_ui import Ui_MainWindow
from gazupublisher.ui_data.ui_values import height_app

from .. import exceptions


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):

    def __init__(self, app):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)

        self.app = app
        self.manage_size()
        self.setup_translation("en_US")
        self.setupUi(self)

    def manage_size(self):
        """
        Manage size policy. Window can't be larger than full screen.
        """
        max_size = self.app.desktop().availableGeometry().size()
        self.setMaximumWidth(max_size.width())
        self.setMaximumHeight(max_size.height())
        self.setSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding
        )

    def setup_translation(self, language_file_name=None):
        language_file_path = self.build_language_file_path(language_file_name)
        translator = QtCore.QTranslator()
        if translator.load(language_file_path):
            self.app.installTranslator(translator)
        else:
            path = os.path.abspath(language_file_path)
            raise exceptions.TranslationException(
                "Loading of the translation file at path %s failed" % path
            )

    def build_language_file_path(self, language_file_name=None):
        if language_file_name is None:
            language_file_name = QtCore.QLocale.system().name()

        current_file_path = os.path.dirname(os.path.realpath(__file__))
        return os.path.join(
            current_file_path,
            "..",
            "..",
            "resources",
            "translations",
            "%s.qm" % language_file_name
        )
