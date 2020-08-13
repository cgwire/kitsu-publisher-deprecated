import datetime
import os
import sys
import traceback

import gazu
import Qt.QtWidgets as QtWidgets
import Qt.QtCore as QtCore
import Qt.QtGui as QtGui

from kitsupublisher.views.MainWindow import MainWindow
from kitsupublisher.ui_data.color import main_color, text_color
from kitsupublisher.utils.error_window import ResizableMessageBox
from kitsupublisher.utils.pyversion import check_module_import
from kitsupublisher.working_context import (
    set_working_context,
    get_working_context,
    is_maya_context,
    is_blender_context,
    is_qt_context,
)
from qtazu.widgets.login import Login


# Hack to allow to close the application with Ctrl+C
import signal

signal.signal(signal.SIGINT, signal.SIG_DFL)

last_failure_time = datetime.datetime.now() - datetime.timedelta(days=1)


def excepthook(exc_type, exc_value, exc_traceback):
    """
    Handle unexpected errors by popping an error window and restarting the app.
    """
    global last_failure_time
    failure_time = datetime.datetime.now()
    difference_with_last_failure = failure_time - last_failure_time
    last_failure_time = failure_time
    if difference_with_last_failure < datetime.timedelta(seconds=2):
        return

    string_tb = traceback.format_exception(exc_type, exc_value, exc_traceback)
    from_kitsupublisher = any(
        "kitsupublisher" in tb_step for tb_step in string_tb
    )
    if not from_kitsupublisher:
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return

    header = "\n=== An error occured !=== \nError message:\n"
    traceback_print = "".join(string_tb)

    message = "%s%s" % (header, traceback_print)
    if is_blender_context():
        from dccutils.dcc_blender import BlenderContext
        BlenderContext.software_print(message)
    else:
        print(message)
    app = QtWidgets.QApplication.instance()
    create_error_dialog(app.current_window, traceback_print)
    app.current_window.close()
    launch_main_window(app)


def create_error_dialog(parent, message):
    """
    Create an error dialog window.
    """
    error_dialog = ResizableMessageBox(parent)
    error_dialog.setWindowTitle("ERROR")
    error_dialog.setModal(True)
    error_dialog.setText("An error has occurred")
    error_dialog.setDetailedText(message)
    error_dialog.setStandardButtons(QtWidgets.QMessageBox.Cancel)
    error_dialog.show()
    error_dialog.raise_()
    error_dialog.activateWindow()


def launch_main_window(app):
    """
    Launch the main window.
    """
    window = create_main_window(app)
    window.show()


def on_emit(is_success, app, login_window):
    """
    Activated on emit from the login window.
    """
    if is_success:
        login_window.deleteLater()
        launch_main_window(app)


def gazu_login_window(app):
    """
    Creates the login window.
    """
    login_window = Login()
    login_window.logged_in.connect(
        lambda is_success: on_emit(is_success, app, login_window)
    )
    return login_window


def setup_dark_mode(app):
    """
    Set up dark mode.
    """
    palette = QtGui.QPalette()
    palette.setColor(QtGui.QPalette.Window, QtGui.QColor(main_color))
    palette.setColor(QtGui.QPalette.WindowText, QtGui.QColor(text_color))
    palette.setColor(QtGui.QPalette.Base, QtGui.QColor(main_color))
    palette.setColor(QtGui.QPalette.AlternateBase, QtGui.QColor(main_color))
    palette.setColor(QtGui.QPalette.ToolTipBase, QtGui.QColor(text_color))
    palette.setColor(QtGui.QPalette.ToolTipText, QtGui.QColor(text_color))
    palette.setColor(QtGui.QPalette.Text, QtGui.QColor(text_color))
    palette.setColor(QtGui.QPalette.Button, QtGui.QColor(main_color))
    palette.setColor(QtGui.QPalette.ButtonText, QtGui.QColor(text_color))
    palette.setColor(QtGui.QPalette.BrightText, QtCore.Qt.red)
    palette.setColor(QtGui.QPalette.Link, QtGui.QColor(42, 130, 218))
    palette.setColor(QtGui.QPalette.Highlight, QtGui.QColor(42, 130, 218))
    palette.setColor(QtGui.QPalette.HighlightedText, QtCore.Qt.black)
    palette.setColor(
        QtGui.QPalette.Disabled,
        QtGui.QPalette.WindowText,
        QtGui.QColor(text_color).darker(170),
    )
    palette.setColor(
        QtGui.QPalette.Disabled,
        QtGui.QPalette.ButtonText,
        QtGui.QColor(text_color).darker(170),
    )
    app.setPalette(palette)


def setup_style(app):
    """
    Setup style. 'Fusion' is the wanted default style for this app.
    Maya already defines its own style.
    """
    if not is_maya_context():
        if "Fusion" in QtWidgets.QStyleFactory.keys():
            app.setStyle("Fusion")
        setup_dark_mode(app)


def create_app():
    """
    If we are in a qt built-in context (Maya, Houdini, ...), an instance of app
    already exists.
    """
    app = QtCore.QCoreApplication.instance()
    if app:
        if check_module_import("maya.cmds"):
            set_working_context("MAYA")
        elif check_module_import("hou"):
            set_working_context("HOUDINI")
    else:
        app = QtWidgets.QApplication(sys.argv)
    setup_style(app)
    sys.excepthook = excepthook
    return app


def create_login_window(app):
    login_window = gazu_login_window(app)
    app.current_window = login_window
    return login_window


def create_main_window(app):
    main_window = MainWindow(app)
    app.current_window = main_window
    main_window.setObjectName("main_window")
    main_window.setWindowTitle("Kitsu Publisher")
    main_window.setStyleSheet(
        "QMainWindow{background-color: %s;} "
        "QToolTip{color: %s; background-color: %s; border: 0px;}"
        % (main_color, text_color, main_color)
    )
    return main_window


def launch_app(app):
    """
    Start Qt event loop if not already started
    """
    if not is_qt_context():
        sys.exit(app.exec_())


def main():
    try:
        app = create_app()
        host = os.environ.get("CGWIRE_HOST", None)
        login = os.environ.get("CGWIRE_LOGIN", None)
        password = os.environ.get("CGWIRE_PASSWORD", None)
        if login is not None and password is not None:
            gazu.set_host(host)
            gazu.log_in(login, password)
            launch_main_window(app)
        else:
            login_window = create_login_window(app)
            login_window.show()
        launch_app(app)

    except KeyboardInterrupt:
        sys.exit()


if __name__ == "__main__":
    print("Working context : " + get_working_context())
    main()
