import sys

import Qt.QtWidgets as QtWidgets
import pytest, unittest.mock as mock
from pytestqt.plugin import QtBot

import gazu
import tests.fixtures as fixtures
import gazupublisher.ui_data.table_headers as headers
from gazupublisher.views.TasksTab import TasksTab


def mock_functions():
    gazu.user.all_tasks_to_do = mock.MagicMock(return_value=fixtures.tasks)
    gazu.task.all_task_statuses = mock.MagicMock(
        return_value=fixtures.status_names
    )
    headers.tab_columns = fixtures.tab_columns


@pytest.fixture(scope="module", autouse=True)
def before_each_test():
    mock_functions()
    app = QtWidgets.QApplication(sys.argv)
    window = QtWidgets.QMainWindow()
    return app, window


def test_wrong_attribute(before_each_test):
    """
    Test the behaviour of the class when asked for an inexisting task attribute
    """
    _, window = before_each_test
    with pytest.raises(AssertionError):
        tab_columns = {
            "task_attribute_that_does_not_exist": "random_column_name"
        }
        TasksTab(window, tab_columns)


def test_sort(before_each_test):
    """
    Test that the table is well sorted
    """
    _, window = before_each_test
    tab_columns = {
        "project_name": "Project Name",
        "task_type_name": "Task type name",
        "entity_name": "Name",
    }
    tasks_table = TasksTab(window, tab_columns)

    header_row_count = tasks_table.rowCount()
    for row in range(1, header_row_count):
        for col in range(len(tab_columns)):
            cell1 = tasks_table.item(row - 1, col)
            cell2 = tasks_table.item(row, col)
            if cell1 != cell2:
                assert cell1 < cell2


def test_creation(before_each_test):
    """
    Test the creation of the table
    """
    _, window = before_each_test
    tasks_table = TasksTab(window, headers.tab_columns)
    header_col_count = tasks_table.columnCount()
    header_row_count = tasks_table.rowCount()
    for row in range(0, header_row_count):
        for col in range(0, header_col_count - 1):
            assert isinstance(
                tasks_table.item(row, col), QtWidgets.QTableWidgetItem
            )
