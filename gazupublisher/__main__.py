import sys
import traceback

import Qt.QtWidgets as QtWidgets
import Qt.QtCore as QtCore
import Qt.QtGui as QtGui

from gazupublisher.views.MainWindow import MainWindow
from gazupublisher.ui_data.color import main_color, text_color
from gazupublisher.utils.error_window import ResizableMessageBox
from gazupublisher.working_context import (
    set_working_context,
    get_working_context,
    is_maya_context,
    is_blender_context,
)
from qtazu.widgets.login import Login


# Hack to allow to close the application with Ctrl+C
import signal

signal.signal(signal.SIGINT, signal.SIG_DFL)


def excepthook(exc_type, exc_value, exc_traceback):
    """
    Handle unexpected errors by popping an error window and restarting the app.
    """

    string_tb = traceback.format_exception(exc_type, exc_value, exc_traceback)
    from_gazupublisher = any(
        "gazupublisher" in tb_step for tb_step in string_tb
    )
    if not from_gazupublisher:
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return

    header = "\n=== An error occured !=== \nError message:\n"
    traceback_print = "".join(string_tb)

    message = "%s%s" % (header, traceback_print)
    if is_blender_context():
        from gazupublisher.utils.blender import blender_print

        blender_print(message)
    else:
        print(message)
    app = QtWidgets.QApplication.instance()
    create_error_dialog(app.current_window, traceback_print)
    app.current_window.close()
    launch_main_app(app)


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


def launch_main_app(app):
    """
    Launch the main application.
    """
    window = create_main_window(app)
    window.show()


def on_emit(is_success, app, login_window):
    """
    Activated on emit from the login window.
    """
    if is_success:
        login_window.deleteLater()
        launch_main_app(app)


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
    if "Fusion" in QtWidgets.QStyleFactory.keys() and not is_maya_context():
        app.setStyle("Fusion")


def create_app():
    app = QtCore.QCoreApplication.instance()
    if app:
        try:
            import maya.cmds

            set_working_context("MAYA")
        except:
            pass
    else:
        app = QtWidgets.QApplication(sys.argv)
    setup_style(app)
    setup_dark_mode(app)
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
    main_window.setWindowTitle("Kitsu")
    main_window.setStyleSheet(
        "QMainWindow{background-color: %s;} "
        "QToolTip{color: %s; background-color: %s; border: 0px;}"
        % (main_color, text_color, main_color)
    )
    return main_window


def main():
    try:
        app = create_app()
        login_window = create_login_window(app)
        login_window.show()
        sys.exit(app.exec_())

    except KeyboardInterrupt:
        sys.exit()


if __name__ == "__main__":
    set_working_context("STANDALONE")
    print("Working context : " + get_working_context())
    main()
