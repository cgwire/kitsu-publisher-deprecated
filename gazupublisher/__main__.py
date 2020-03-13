import sys
import gazu
import Qt.QtWidgets as QtWidgets


from gazupublisher.views.MainWindow import MainWindow
from gazupublisher.views.TasksTab import TasksTab
import utils, config

def main():
    app = QtWidgets.QApplication(sys.argv)

    utils.configure_host("http://localhost/api")
    utils.connect_user("admin@example.com", "mysecretpassword")

    # window = QtWidgets.QMainWindow()
    # window.show()

    print(gazu.user.all_tasks_to_do())
    print(gazu.task.all_task_types())

    tb = TasksTab(config.tab_columns)
    tb.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
