import os

from Qt import QtCore, QtWidgets

from kitsupublisher.views.MainWindow_ui import Ui_MainWindow
from kitsupublisher.views.Worker import Worker
from kitsupublisher.utils.file import load_translation_files
from kitsupublisher.utils.connection import configure_event_host, create_event

from kitsupublisher import exceptions


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    update_table = QtCore.Signal()

    def __init__(self, app, real_time=True):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)

        self.app = app
        self.manage_size()

        try:
            self.setup_translation("en_US")
        except Exception:
            pass
        self.setupUi(self)

        self.set_up_main_gui_listeners()
        self.threadpool = QtCore.QThreadPool.globalInstance()

        if real_time:
            try:
                self.toolbar.reload_btn.hide()
                self.launch_real_time_thread()
            except Exception:
                self.toolbar.reload_btn.show()

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
        self.layout().setSizeConstraint(QtWidgets.QLayout.SetFixedSize)

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

        return load_translation_files(language_file_name)

    def set_up_main_gui_listeners(self):
        """
        To ensure proper Qt behaviour, communication between threads must be
        handled by signals. When a change is detected in the db, it launches the
        table_updated function, which itself emits the update_table signal. It's
        worth noting that there are two kind of listeners here (one for each
        thread), and that they communicate through a function (here
        self.table_updated)
        """
        self.update_table.connect(self.reload)

    def set_up_thread_listeners(self):
        configure_event_host()
        events = [
            "task:update",
            "task:assign",
            "task:unassign",
            "task:status-change",
        ]
        create_event(events, self.table_updated)

    def launch_real_time_thread(self):
        """
        Launch a parallel thread.
        This thread will listen to any update event from the db and send signals
        to the main GUI thread accordingly.
        """
        self.worker = Worker(self.set_up_thread_listeners)
        self.threadpool.start(self.worker)

    def table_updated(self, data):
        self.update_table.emit()

