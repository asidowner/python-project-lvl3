import pytest

from page_loader.lib.name_generator import get_html_name_from_url, \
    get_file_name_from_url, \
    get_file_dir_name_from_url


@pytest.mark.parametrize('url,expected',
                         [
                             (
                                 'https://google.com',
                                 'google-com_files'
                             ),
                             (
                                 'https://google.com?a=b',
                                 'google-com-a-b_files'
                             ),
                             (
                                 'https://google.com/path/to/some.jpg',
                                 'google-com-path-to-some_files'
                             )
                         ])
def test_get_files_dir_from_url(url, expected):
    assert get_file_dir_name_from_url(url) == expected


@pytest.mark.parametrize('url,expected',
                         [
                             (
                                 'https://google.com',
                                 'google-com.html'
                             ),
                             (
                                 'https://google.com?a=b',
                                 'google-com-a-b.html'
                             ),
                             (
                                 'https://google.com/path/to/some.jpg',
                                 'google-com-path-to-some.jpg'
                             )
                         ])
def test_get_file_name_from_url(url, expected):
    assert get_file_name_from_url(url) == expected


@pytest.mark.parametrize('url,expected',
                         [
                             (
                                 'https://google.com',
                                 'google-com.html'
                             ),
                             (
                                 'https://google.com?a=b',
                                 'google-com-a-b.html'
                             ),
                             (
                                 'https://google.com/path/to/some.jpg',
                                 'google-com-path-to-some.html'
                             )
                         ])
def test_get_html_name_from_url(url, expected):
    assert get_html_name_from_url(url) == expected
