import sys
import os
import gazu
<<<<<<< HEAD
import random
import Qt.QtWidgets as QtWidgets
=======
>>>>>>> 49a8687dc77b8b6043caa2674fd074d0d45b0248

import Qt.QtWidgets as QtWidgets
import Qt.QtCore as QtCore

from gazupublisher.views.MainWindow import MainWindow
<<<<<<< HEAD
# import tests.utils as tests_utils
#
# from inspect import getmembers, isfunction
import utils



def main():

# Hack to allow to close the application with Ctrl+C
import signal
signal.signal(signal.SIGINT, signal.SIG_DFL)


def main():
    try:
        if os.getenv("DEBUG", False):
            gazu.set_host("http://localhost:8080/api")
            gazu.log_in("admin@example.com", "mysecretpassword")
            os.environ["CGWIRE_HOST"] = "http://localhost:8080/api"

        app = QtWidgets.QApplication(sys.argv)
        app.setApplicationDisplayName(
            QtCore.QCoreApplication.translate("Application", "Name")
        )
        window = MainWindow(app)
        window.show()

        sys.exit(app.exec_())
    except KeyboardInterrupt:
        sys.exit()


if __name__ == "__main__":
    main()
