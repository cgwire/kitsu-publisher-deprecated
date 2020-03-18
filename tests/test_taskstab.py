import sys
import gazu
import unittest

import tests.utils_tests as utils_tests
from gazupublisher.views.TasksTab import TasksTab
from gazupublisher import config

import Qt.QtWidgets as QtWidgets


class TasksTabTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """
        Code that wil run once at the beginning of the test session.
        Here, we handle the connection to the Gazu API and the creation of the environnment
        """
        utils_tests.connect()
        cls.app = QtWidgets.QApplication(sys.argv)
        cls.window = QtWidgets.QMainWindow()
        cls.project_name = "TestProjectToDelete"

    def setUp(self):
        """
        Code that will run before each test.
        Here, we regenerate the datas of the table
        """
        self.project_dict = utils_tests.generate_project(self.project_name)

    def tearDown(self):
        """
        Code that will run after each test.
        """
        pass

    @classmethod
    def tearDownClass(cls):
        """
        Code that will run at the end of the test session.
        Here, we delete the project created for the occasion
        """
        utils_tests.delete_project_from_name(cls.project_name)

    def test_wrong_attribute(self):
        """
        Test the behaviour of the class when asked for an inexisting task attribute
        """
        with self.assertRaises(AssertionError):
            tab_columns = {"task_attribute_that_does_not_exist": "random_column_name"}
            TasksTab(self.window, tab_columns)

    def test_sort(self):
        """
        Test that the table is well sorted
        """
        sort_id = "created_at"
        tab_columns = {"created_at": "Creation date", "entity_name": "Nom"}
        tasks_table = TasksTab(self.window, tab_columns, sort_id)

        pos_col_sort = tasks_table.horizontalHeader().sortIndicatorSection()
        header_row_count = tasks_table.rowCount()
        for row in range(1, header_row_count):
            cell1 = tasks_table.item(row - 1, pos_col_sort).text()
            cell2 = tasks_table.item(row, pos_col_sort).text()
            assert(cell1 <= cell2)

    def test_creation(self):
        """
        Test the creation of the table
        """
        tasks_table = TasksTab(self, config.tab_columns)
        header_col_count = tasks_table.columnCount()
        header_row_count = tasks_table.rowCount()
        for row in range(0, header_row_count):
            for col in range(0, header_col_count-1):
                print(tasks_table.item(row, col))
                assert(isinstance(tasks_table.item(row, col), QtWidgets.QTableWidgetItem))
            assert(isinstance(tasks_table.cellWidget(row, header_col_count-1), QtWidgets.QPushButton))
