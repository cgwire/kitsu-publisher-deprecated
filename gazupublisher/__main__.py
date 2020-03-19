import sys
import gazu
import random
import Qt.QtWidgets as QtWidgets


from gazupublisher.views.MainWindow import MainWindow
# import tests.utils as tests_utils
#
# from inspect import getmembers, isfunction
import utils.connection as utils_co
import utils.data as utils_data



def main():

    utils_co.configure_host("http://localhost/api")
    utils_co.connect_user("admin@example.com", "mysecretpassword")

    print(utils_data.get_all_tasks_to_do()[0])

    app = QtWidgets.QApplication(sys.argv)
    win = MainWindow(app)

    app.setApplicationDisplayName(app.translate("ApplicationDisplayName", "Main application name"))
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
