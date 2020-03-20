import sys
import gazu
import unittest

import tests.utils_tests as utils_tests
from gazupublisher.views.TasksTab import TasksTab
import gazupublisher.utils.data as utils_data
import unittest.mock as mock
from gazupublisher import config

import Qt.QtWidgets as QtWidgets


class TasksTabTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """
        Code that wil run once at the beginning of the test session.
        Here, we initiate the app environment, and we mock the data from the gazu API needed by the app
        """
        cls.app = QtWidgets.QApplication(sys.argv)
        cls.window = QtWidgets.QMainWindow()

        cls.mock_data = utils_tests.MockResponse
        gazu.user.all_tasks_to_do = mock.MagicMock(return_value=cls.mock_data.tasks())
        gazu.task.all_task_statuses = mock.MagicMock(return_value=cls.mock_data.status_names())


    def test_wrong_attribute(self):
        """
        Test the behaviour of the class when asked for an inexisting task attribute
        """
        with self.assertRaises(AssertionError):
            tab_columns = {"task_attribute_that_does_not_exist": "random_column_name"}
            TasksTab(self.window, tab_columns)

    def test_creation(self):
        """
        Test the creation of the table
        """
        tasks_table = TasksTab(self.window, self.mock_data.tab_columns())
        header_col_count = tasks_table.columnCount()
        header_row_count = tasks_table.rowCount()
        for row in range(0, header_row_count):
            for col in range(0, header_col_count-1):
                assert(isinstance(tasks_table.item(row, col), QtWidgets.QTableWidgetItem))
            assert(isinstance(tasks_table.cellWidget(row, header_col_count-1), QtWidgets.QPushButton))

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

