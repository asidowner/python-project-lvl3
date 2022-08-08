from random import randint

import pytest
import os
import requests
import requests_mock
from requests_mock import Adapter
from requests import Session
from page_loader import download


def path_to_fixtures(name: str) -> str:
    return os.path.join('tests', 'fixtures', name)


@pytest.fixture
def data_to_download() -> str:
    with open(path_to_fixtures('index.html'), encoding='utf8') as f:
        return f.read()


@pytest.fixture
def mock_url() -> str:
    return 'mock://ru.test.com/project/51.json?a=b'


@pytest.fixture
def expected_f_name() -> str:
    return 'ru-test-com-project-51-a-b.html'


@pytest.fixture
def mock_session(data_to_download, mock_url):
    session = requests.Session()
    adapter = requests_mock.Adapter()
    session.mount('mock://', adapter)
    adapter.register_uri('GET', mock_url, text=data_to_download)
    return session


def test_downloaded_file_name(tmpdir, mock_session, mock_url, expected_f_name):
    file_path = download(mock_url, tmpdir, mock_session)
    assert file_path == tmpdir.join(expected_f_name)


def test_download(tmpdir, mock_session, mock_url, expected_f_name, data_to_download):
    file_path = download(mock_url, tmpdir, mock_session)
    with open(file_path, 'r', encoding='utf8') as f:
        assert f.read() == data_to_download


def test_raise_if_dir_not_found(mock_session, mock_url):
    with pytest.raises(NotADirectoryError):
        download(mock_url, '/unknown/dir/path', mock_session)
