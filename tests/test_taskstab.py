import sys

import Qt.QtWidgets as QtWidgets
import pytest, unittest.mock as mock

import gazu
from tests.fixtures import fixtures
import gazupublisher.ui_data.table_headers as headers
from gazupublisher.views.TasksTab import TasksTab
from gazupublisher.views.MainWindow import MainWindow


def mock_table_functions():
    gazu.user.all_tasks_to_do = mock.MagicMock(return_value=fixtures.tasks)
    gazu.task.all_task_statuses = mock.MagicMock(
        return_value=fixtures.status_names
    )
    headers.tab_columns = fixtures.tab_columns

def mock_panel_functions():
    gazu.files.get_all_preview_files_for_task = mock.MagicMock(
        return_value=fixtures.all_preview_files_for_task
    )
    gazu.task.all_comments_for_task = mock.MagicMock(
        return_value=fixtures.all_comments_for_task
    )
    gazu.task.get_last_comment_for_task = mock.MagicMock(
        return_value=fixtures.all_comments_for_task[0]
    )

@pytest.fixture(scope="module", autouse=True)
def before_each_test():
    mock_table_functions()
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow(app, real_time=False)
    return app, window


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


def test_panel_initialization(before_each_test):
    """
    Test the panel initialization
    """
    app, window = before_each_test
    mock_panel_functions()
    tab_columns = {
        "project_name": "Project Name",
        "task_type_name": "Task type name",
        "entity_name": "Name",
    }
    tasks_table = TasksTab(window, tab_columns)
    item = tasks_table.item(0, 0)
    tasks_table.setCurrentItem(item)
    tasks_table.on_click()
    assert hasattr(window, "task_panel")
    assert window.task_panel.task == item.task
    assert window.task_panel.task_panel_vertical_layout.count() == 4
