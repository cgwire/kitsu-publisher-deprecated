import gazu

from unittest import mock
from gazupublisher.utils import data as data_utils

from tests import fixtures

gazu.project.all_open_projects = mock.MagicMock(
    return_value=fixtures.open_projects
)


def test_get_all_open_project_names():
    names = data_utils.get_all_open_project_names()
    assert names == ["Agent 327", "Caminandes"]
