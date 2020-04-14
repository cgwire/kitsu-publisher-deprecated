import requests.exceptions
import pytest
from unittest import mock
import gazu

from gazupublisher.utils import connection as connection_utils

from tests import fixtures


gazu.client.make_auth_header = mock.MagicMock(return_value=fixtures.auth_header)


def test_get_data_from_true_url():
    url = "http://localhost/img/kitsu.b07d6464.png"
    data = connection_utils.get_file_data_from_url(url, full=True)
    assert data.content


def test_get_data_from_inexisting_url():
    url = "https://url-that-does-not-exist"
    with pytest.raises(requests.exceptions.ConnectionError):
        connection_utils.get_file_data_from_url(url)

def test_get_all_open_project_names():
    auth_header = connection_utils.get_auth_header()
    assert auth_header == {
    "Authorization": "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE1ODYxNjEyMTcsIm5iZiI6MTU4NjE2MTIxNywianRpIjoiYWJlNTMzODgtZjZiMy00MjBkLTlmMWYtODY2NDliZmY0YzU5IiwiZXhwIjoxNTg2NzY2MDE3LCJpZGVudGl0eSI6ImFkbWluQGV4YW1wbGUuY29tIiwiZnJlc2giOmZhbHNlLCJ0eXBlIjoiYWNjZXNzIn0.S92hyy_6joPKbx6_fiM3hgS7PVLZYQaAgLdeYzxV0WQ"
}