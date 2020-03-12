import sys
import gazu
import unittest

from gazupublisher import utils
from gazupublisher.views.TasksTab import TasksTab

import Qt.QtWidgets as QtWidgets



class TasksTabTestCase(unittest.TestCase):
    def test_wrong_attribute(self):
        """
        Test the behaviour of the class when asked for an inexisting task attribute
        """
        utils.configure_host("http://localhost/api")
        utils.connect_user("admin@example.com", "mysecretpassword")
        with self.assertRaises(AssertionError):
            tab_columns = {"task_attribute_that_does_not_exist": "random_column_name"}
            tb = TasksTab(tab_columns)
            tb.show()

    # def test_wrong_connection(self):
    #     """
    #     Test the behaviour of the class when there is no connexion
    #     """
    #
    #     with self.assertRaises(ConnectionError):
    #         tab_columns = {"id": "Identifiant"}
    #         tb = TasksTab(tab_columns)
    #         tb.show()