import sys
import gazu
import Qt.QtWidgets as QtWidgets


from gazupublisher.views.MainWindow import MainWindow
from gazupublisher.views.TasksTab import TasksTab


import utils, config

def main():
    app = QtWidgets.QApplication(sys.argv)

    if utils.qtazu_login():
        tasks_table = TasksTab(config.tab_columns)
        tasks_table.show()
        sys.exit(app.exec_())


if __name__ == "__main__":
    main()
