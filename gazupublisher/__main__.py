import sys
import os
import gazu

import Qt.QtWidgets as QtWidgets
import Qt.QtCore as QtCore

from gazupublisher.views.MainWindow import MainWindow


def main():
    if os.getenv("DEBUG", False):
        gazu.set_host("http://localhost:8080/api")
        gazu.log_in("admin@example.com", "mysecretpassword")
        os.environ["CGWIRE_HOST"] = "http://localhost:8080/api"

    app = QtWidgets.QApplication(sys.argv)
    app.setApplicationDisplayName(
        QtCore.QCoreApplication.translate(
            "ApplicationDisplayName", "Main application name")
        )
    window = MainWindow(app)
    window.show()
    sys.exit(app.exec_())

    """
    if utils.qtazu_login():
        tasks_table = TasksTab(config.tab_columns)
        tasks_table.show()
        sys.exit(app.exec_())
    """


if __name__ == "__main__":
    main()
