import pytest
import os
import requests
import requests_mock
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
def expected_img_dir_name() -> str:
    return 'ru-test-com-project-51-a-b_files'


@pytest.fixture
def expected_img_name() -> str:
    return 'ru-test-com-img.png'


@pytest.fixture
def expected_img_url() -> str:
    return 'mock://ru.test.com/ru-test-com-img.png'


@pytest.fixture
def expected_img_path(expected_img_dir_name,
                      expected_img_name) -> str:
    return path_to_fixtures('img.png')


@pytest.fixture
def expected_html(expected_img_dir_name, expected_img_name) -> str:
    with open(path_to_fixtures('expected_index.html'), encoding='utf8') as f:
        return f.read()


@pytest.fixture
def mock_session(data_to_download,
                 mock_url,
                 expected_img_url,
                 expected_img_path):
    session = requests.Session()
    adapter = requests_mock.Adapter()
    session.mount('mock://', adapter)
    adapter.register_uri('GET', mock_url, text=data_to_download)
    with open(expected_img_path, 'rb') as f:
        adapter.register_uri('GET', expected_img_url, content=f.read())
    return session


def test_downloaded_file_name(tmpdir, mock_session, mock_url, expected_f_name):
    file_path = download(mock_url, tmpdir, mock_session)
    assert file_path == tmpdir.join(expected_f_name)


def test_download(tmpdir,
                  mock_session,
                  mock_url,
                  expected_html):
    file_path = download(mock_url, tmpdir, mock_session)
    with open(file_path, 'r', encoding='utf8') as f:
        assert f.read() == expected_html


def test_image_download(tmpdir,
                        mock_session,
                        mock_url,
                        expected_img_name):
    file_path = download(mock_url, tmpdir, mock_session)
    path_to_image_dir = file_path.replace('.html', '_files')
    assert os.path.isdir(path_to_image_dir)

    image_path = os.path.join(path_to_image_dir, expected_img_name)
    assert os.path.isfile(image_path)


def test_raise_if_dir_not_found(mock_session, mock_url):
    with pytest.raises(NotADirectoryError):
        download(mock_url, '/unknown/dir/path', mock_session)
