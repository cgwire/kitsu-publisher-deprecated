import sys
import os
import gazu

import Qt.QtWidgets as QtWidgets
import Qt.QtCore as QtCore

from gazupublisher.views.MainWindow import MainWindow


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
