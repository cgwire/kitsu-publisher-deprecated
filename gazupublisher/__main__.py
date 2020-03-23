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


def gazu_login_window():
    login_window = Login()
    login_window.exec()
    return login_window.result()


def main():
    try:
        app = QtWidgets.QApplication(sys.argv)
        app.setApplicationDisplayName(
            QtCore.QCoreApplication.translate("Application", "Name")
        )
        if gazu_login_window():
            window = MainWindow(app)
            window.show()
            sys.exit(app.exec_())

    except KeyboardInterrupt:
        sys.exit()


if __name__ == "__main__":
    main()
