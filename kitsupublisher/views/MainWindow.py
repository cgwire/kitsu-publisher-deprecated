import os

from Qt import QtCore, QtWidgets

from kitsupublisher.views.MainWindow_ui import Ui_MainWindow
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
        if real_time:
            try:
                self.toolbar.reload_btn.hide()
                self.launch_thread()
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
        handled by signals. This results in two sets of listeners (for the two
        threads), which basically do the same.
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

    def launch_thread(self):
        """
        Launch a parallel thread.
        This thread will listen to any update event from the db and send signals
        to the main GUI thread accordingly.
        """
        self.threadpool = QtCore.QThreadPool()
        self.worker = Worker(self.set_up_thread_listeners)
        self.threadpool.start(self.worker)

    def table_updated(self, data):
        self.update_table.emit()


class Worker(QtCore.QRunnable):
    """
    Worker thread
    :param callback: The function callback to run on this worker thread.
                     Supplied args and kwargs will be passed through to the runner.
    :type callback: function
    :param args: Arguments to pass to the callback function
    :param kwargs: Keywords to pass to the callback function

    """

    def __init__(self, function, *args, **kwargs):
        super(Worker, self).__init__()

        self.function = function
        self.args = args
        self.kwargs = kwargs

    @QtCore.Slot()
    def run(self):
        """
        Initialise the runner function with passed args, kwargs.
        """
        self.function(*self.args, **self.kwargs)
