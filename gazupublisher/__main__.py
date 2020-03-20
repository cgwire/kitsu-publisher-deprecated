import sys
import gazu
import random
import Qt.QtWidgets as QtWidgets
import Qt.QtCore as QtCore


from gazupublisher.views.MainWindow import MainWindow
from gazupublisher.utils.data import get_task_status_names

# import tests.utils as tests_utils
#
# from inspect import getmembers, isfunction
import utils.connection as utils_co
import utils.data as utils_data



def main():

    utils_co.configure_host("http://localhost/api")
    utils_co.connect_user("admin@example.com", "mysecretpassword")

    print(gazu.task.all_task_statuses())

    app = QtWidgets.QApplication(sys.argv)
    app.setApplicationDisplayName(QtCore.QCoreApplication.translate("ApplicationDisplayName", "Main application name"))
    # app.setApplicationDisplayName(app.tr("ApplicationDisplayName", "Main application name"))
    win = MainWindow(app)


    win.show()
    sys.exit(app.exec_())

    # http://localhost/api
    # admin@example.com
    # mysecretpassword

    # if utils.qtazu_login():
    #     win = MainWindow()
    #     win.show()
    #     sys.exit(app.exec_())


if __name__ == "__main__":
    main()
