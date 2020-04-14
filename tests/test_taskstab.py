import sys

import Qt.QtWidgets as QtWidgets
import Qt.QtCore as QtCore
import pytest, unittest.mock as mock
from pytestqt.plugin import QtBot

import gazu
import tests.fixtures as fixtures
import gazupublisher.ui_data.table_headers as headers
from gazupublisher.views.TasksTab import TasksTab


def mock_functions():
    gazu.user.all_tasks_to_do = mock.MagicMock(return_value=fixtures.tasks)
    gazu.task.all_task_statuses = mock.MagicMock(
        return_value=fixtures.status_names)
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
            "task_attribute_that_does_not_exist": "random_column_name"}
        TasksTab(window, tab_columns)


def test_sort(before_each_test):
    """
    Test that the table is well sorted
    """
    _, window = before_each_test
    sort_id = "created_at"
    tab_columns = {"created_at": "Creation date", "entity_name": "Nom"}
    tasks_table = TasksTab(window, tab_columns)

    pos_col_sort = tasks_table.horizontalHeader().sortIndicatorOrder()
    is_ascending = (pos_col_sort == QtCore.Qt.AscendingOrder)
    header_row_count = tasks_table.rowCount()
    for row in range(1, header_row_count):
        cell1 = tasks_table.item(row - 1, pos_col_sort).text()
        cell2 = tasks_table.item(row, pos_col_sort).text()
        assert (cell1 <= cell2 if is_ascending else cell1 >= cell2)


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
            assert (isinstance(tasks_table.item(row, col),
                               QtWidgets.QTableWidgetItem))
        assert (isinstance(tasks_table.cellWidget(row, header_col_count - 1),
                           QtWidgets.QPushButton))


def test_comment_window(before_each_test):
    """
    Test if the comment window is correctly instanciated
    """
    def handle_dialog():
        assert button.comment_window
        button.comment_window.done(1)
    app, window = before_each_test
    tasks_table = TasksTab(window, headers.tab_columns)
    header_col_count = tasks_table.columnCount()
    header_row_count = tasks_table.rowCount()
    qtbot = QtBot(app)
    for row in range(0, header_row_count):
        button = tasks_table.cellWidget(row, header_col_count - 1)
        assert (not button.comment_window)
        QtCore.QTimer.singleShot(100, handle_dialog)
        qtbot.mouseClick(button, QtCore.Qt.LeftButton, delay=1)
