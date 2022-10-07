import pytest
import os

from requests import ConnectTimeout
from requests_mock import Mocker


def path_to_fixtures(name: str) -> str:
    return os.path.join('tests', 'fixtures', name)


@pytest.fixture
def base_mock_url() -> str:
    return 'https://ru.test.com'


@pytest.fixture
def expected_f_name() -> str:
    return 'ru-test-com-project-51-a-b.html'


@pytest.fixture
def expected_files_dir_name() -> str:
    return 'ru-test-com-project-51-a-b_files'


@pytest.fixture
def expected_html() -> str:
    with open(path_to_fixtures('expected_index.html'), encoding='utf8') as f:
        return f.read()


@pytest.fixture
def main_html_url(base_mock_url):
    return f'{base_mock_url}/project/51.json?a=b'


@pytest.fixture
def html_url_with_404(base_mock_url):
    return f'{base_mock_url}/test_error'


@pytest.fixture
def html_url_with_file_404(base_mock_url):
    return f'{base_mock_url}/file_error'


@pytest.fixture
def html_url_to_image(base_mock_url):
    return f'{base_mock_url}/img.png'


@pytest.fixture
def url_with_timeout(base_mock_url, requests_mock):
    timeout_url = f'{base_mock_url}/timeout'
    requests_mock.get(timeout_url,
                      exc=ConnectTimeout
                      )
    return timeout_url


@pytest.fixture
def mock_data(base_mock_url,
              main_html_url,
              html_url_with_404,
              html_url_with_file_404):
    return [
        (
            main_html_url,
            path_to_fixtures('index.html'),
            200
        ),
        (
            f'{base_mock_url}/img.png',
            path_to_fixtures('img.png'),
            200
        ),
        (
            f'{base_mock_url}/script1.js',
            path_to_fixtures('script1.js'),
            200
        ),
        (
            f'{base_mock_url}/script2.js',
            path_to_fixtures('script2.js'),
            200
        ),
        (
            f'{base_mock_url}/simple.css',
            path_to_fixtures('simple.css'),
            200
        ),
        (
            f'{base_mock_url}/simple1.css',
            path_to_fixtures('simple.css'),
            200
        ),
        (
            html_url_with_file_404,
            path_to_fixtures('index_error.html'),
            200
        ),
        (
            html_url_with_404,
            None,
            404
        ),
    ]


@pytest.fixture
def expected_additional_files_names(expected_files_dir_name):
    return [
        os.path.join(expected_files_dir_name, 'ru-test-com-img.png'),
        os.path.join(expected_files_dir_name, 'ru-test-com-script1.js'),
        os.path.join(expected_files_dir_name, 'ru-test-com-script2.js'),
        os.path.join(expected_files_dir_name, 'ru-test-com-simple.css')
    ]


@pytest.fixture
def expected_href_file_name(expected_files_dir_name):
    return os.path.join(expected_files_dir_name, 'ru-test-com-simple1.css')


@pytest.fixture
def mock_session(mock_data, requests_mock: Mocker):
    for url, data, status_code in mock_data:
        if data:
            with open(data, 'rb') as f:
                requests_mock.get(url,
                                  status_code=status_code,
                                  content=f.read())
        else:
            requests_mock.get(url, status_code=status_code)
    return requests_mock
