import pytest
import os
from page_loader import download
from page_loader.utils.exception import GetSiteDataError
from page_loader.utils.exception import RequestUrlTimeoutError


def test_downloaded_file_name(tmpdir,
                              main_html_url,
                              mock_session,
                              expected_f_name):
    file_path = download(main_html_url, tmpdir)
    assert file_path == tmpdir.join(expected_f_name)


def test_download(tmpdir,
                  mock_session,
                  main_html_url,
                  expected_html):
    file_path = download(main_html_url, tmpdir)
    with open(file_path, 'r', encoding='utf8') as f:
        assert f.read() == expected_html


def test_files_download(tmpdir,
                        mock_session,
                        main_html_url,
                        expected_files_dir_name,
                        expected_additional_files_names):
    download(main_html_url, tmpdir)
    path_to_files_dir = os.path.join(tmpdir, expected_files_dir_name)
    assert os.path.isdir(path_to_files_dir)

    for file_path in expected_additional_files_names:
        assert os.path.isfile(os.path.join(tmpdir, file_path))


def test_file_with_href_not_downloaded(tmpdir,
                                       mock_session,
                                       main_html_url,
                                       expected_files_dir_name,
                                       expected_href_file_name):
    download(main_html_url, tmpdir)
    assert not os.path.isfile(os.path.join(tmpdir,
                                           expected_files_dir_name,
                                           expected_href_file_name))


def test_raise_if_dir_not_found(main_html_url, mock_session):
    with pytest.raises(NotADirectoryError):
        download(main_html_url, '/unknown/dir/path')


def test_raise_if_site_not_available_error(tmpdir, mock_session,
                                           html_url_with_404):
    with pytest.raises(GetSiteDataError):
        download(html_url_with_404, tmpdir)


def test_raise_if_file_not_available_error(tmpdir, mock_session,
                                           html_url_with_file_404):
    with pytest.raises(GetSiteDataError):
        download(html_url_with_file_404, tmpdir)


def test_raise_timeout_error(tmpdir, mock_session, url_with_timeout):
    with pytest.raises(RequestUrlTimeoutError):
        download(url_with_timeout, tmpdir)
