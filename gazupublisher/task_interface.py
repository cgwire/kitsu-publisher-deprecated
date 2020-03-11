import sys
import gazu

import Qt.QtWidgets as QtWidgets

from views.TasksTab import TasksTab

def connect_user(user, password):
    """
    Log in kitsu
    """
    gazu.log_in(user, password)


def connect_host(host):
    """
    Connexion to the gazu API
    """
    gazu.client.set_host(host)

def main():
    app = QtWidgets.QApplication(sys.argv)

    connect_host("http://localhost/api")
    connect_user("admin@example.com", "mysecretpassword")

    # window = QtWidgets.QMainWindow()
    # window.show()

    # TODO {taskAttribute:columnName}. Columns displayed in the interface. Hardcoded -> Should be put in a config.py or handled somewhere
    tab_columns = {"entity_name": "Nom", "task_type_name": "Type de tâche", "created_at": "Date de création", "last_comment":"Commentaire"}
    tb = TasksTab(tab_columns)
    tb.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()