import gazu

from unittest import mock
from gazupublisher.utils import data as data_utils

from tests.fixtures import fixtures

gazu.project.all_open_projects = mock.MagicMock(
    return_value=fixtures.open_projects
)
gazu.task.all_task_statuses = mock.MagicMock(
    return_value=fixtures.status_names
)
gazu.user.all_tasks_to_do = mock.MagicMock(
    return_value=fixtures.tasks
)

def test_get_all_open_project_names():
    names = data_utils.get_all_open_project_names()
    assert names == ["Agent 327", "Caminandes"]


def test_get_task_status():
    statuses = gazu.task.all_task_statuses()
    list_status = []
    for status in statuses:
        list_status.append(status["name"])
    assert sorted(list_status) == ['Done', 'Retake', 'Todo',
                                   'Waiting For Approval', 'Work In Progress']

def test_get_all_tasks_to_do():
    tasks = gazu.user.all_tasks_to_do()
    list_tasks = []
    for task in tasks:
        list_tasks.append(task["id"])
    assert sorted(list_tasks) == ['4034af63-9a26-42d4-87e2-e86d1446a584',
                                  'e71d0286-cfff-4651-bc64-680caa91c382']
