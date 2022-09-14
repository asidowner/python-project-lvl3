import pytest
import os
import requests
import requests_mock
from page_loader import download
from page_loader.utils.exception import SiteNotAvailableError
from page_loader.utils.exception import FileNotAvailableError


def path_to_fixtures(name: str) -> str:
    return os.path.join('tests', 'fixtures', name)


@pytest.fixture
def data_to_download() -> str:
    with open(path_to_fixtures('index.html'), encoding='utf8') as f:
        return f.read()


@pytest.fixture
def base_mock_url() -> str:
    return 'mock://ru.test.com/'


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
    return base_mock_url + 'project/51.json?a=b'


@pytest.fixture
def html_url_with_404(base_mock_url):
    return base_mock_url + 'test_error'


@pytest.fixture
def html_url_with_file_404(base_mock_url):
    return base_mock_url + 'file_error'


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
            base_mock_url + 'img.png',
            path_to_fixtures('img.png'),
            200
        ),
        (
            base_mock_url + 'script1.js',
            path_to_fixtures('script1.js'),
            200
        ),
        (
            base_mock_url + 'script2.js',
            path_to_fixtures('script2.js'),
            200
        ),
        (
            base_mock_url + 'simple.css',
            path_to_fixtures('simple.css'),
            200
        ),
        (
            base_mock_url + 'simple1.css',
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
def mock_session(data_to_download,
                 mock_data):
    session = requests.Session()
    adapter = requests_mock.Adapter()
    session.mount('mock://', adapter)
    for url, data, status_code in mock_data:
        if data:
            with open(data, 'rb') as f:
                adapter.register_uri('GET',
                                     url,
                                     status_code=status_code,
                                     content=f.read())
        else:
            adapter.register_uri('GET', url, status_code=status_code)
    return session


def test_downloaded_file_name(tmpdir,
                              mock_session,
                              main_html_url,
                              expected_f_name):
    file_path = download(main_html_url, tmpdir, mock_session)
    assert file_path == tmpdir.join(expected_f_name)


def test_download(tmpdir,
                  mock_session,
                  main_html_url,
                  expected_html):
    file_path = download(main_html_url, tmpdir, mock_session)
    with open(file_path, 'r', encoding='utf8') as f:
        assert f.read() == expected_html


def test_files_download(tmpdir,
                        mock_session,
                        main_html_url,
                        expected_files_dir_name,
                        expected_additional_files_names):
    download(main_html_url, tmpdir, mock_session)
    path_to_files_dir = os.path.join(tmpdir, expected_files_dir_name)
    assert os.path.isdir(path_to_files_dir)

    for file_path in expected_additional_files_names:
        assert os.path.isfile(os.path.join(tmpdir, file_path))


def test_file_with_href_not_downloaded(tmpdir,
                                       mock_session,
                                       main_html_url,
                                       expected_files_dir_name,
                                       expected_href_file_name):
    download(main_html_url, tmpdir, mock_session)
    assert not os.path.isfile(os.path.join(tmpdir,
                                           expected_files_dir_name,
                                           expected_href_file_name))


def test_raise_if_dir_not_found(mock_session, main_html_url):
    with pytest.raises(NotADirectoryError):
        download(main_html_url, '/unknown/dir/path', mock_session)


def test_raise_if_site_not_available_error(tmpdir,
                                           mock_session,
                                           html_url_with_404):
    with pytest.raises(SiteNotAvailableError):
        download(html_url_with_404, tmpdir, mock_session)


def test_raise_if_file_not_available_error(tmpdir,
                                           mock_session,
                                           html_url_with_file_404):
    with pytest.raises(FileNotAvailableError):
        download(html_url_with_file_404, tmpdir, mock_session)
