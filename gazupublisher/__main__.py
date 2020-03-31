import sys
import os
import gazu

import Qt.QtWidgets as QtWidgets
import Qt.QtCore as QtCore

from gazupublisher.views.MainWindow import MainWindow
from qtazu.widgets.login import Login

# Hack to allow to close the application with Ctrl+C
import signal

signal.signal(signal.SIGINT, signal.SIG_DFL)


def launch_main_app(app):
    """
    Launch the main application.
    """
    window = MainWindow(app)
    window.show()


def on_emit(emit, app):
    """
    Activated on emit from the login window.
    """
    if emit:
        launch_main_app(app)

def gazu_login_window(app):
    """
    Creates the login window.
    """
    login_window = Login()
    login_window.logged_in.connect(lambda emit: on_emit(emit, app))
    return login_window


def main():
    try:
        app = QtWidgets.QApplication(sys.argv)
        app.setApplicationDisplayName(
            QtCore.QCoreApplication.translate("Application", "Name")
        )
        login_window = gazu_login_window(app)
        login_window.show()
        sys.exit(app.exec_())

    except KeyboardInterrupt:
        sys.exit()


if __name__ == "__main__":
    main()
