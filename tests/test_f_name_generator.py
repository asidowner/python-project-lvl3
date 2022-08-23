import pytest

from page_loader.lib.name_generator import get_html_name_from_url
from page_loader.lib.name_generator import get_image_name_from_url
from page_loader.lib.name_generator import get_image_dir_name_from_url


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
def test_get_image_dir_from_url(url, expected):
    assert get_image_dir_name_from_url(url) == expected


@pytest.mark.parametrize('url,expected',
                         [
                             (
                                 'https://google.com',
                                 'google-com'
                             ),
                             (
                                 'https://google.com?a=b',
                                 'google-com-a-b'
                             ),
                             (
                                 'https://google.com/path/to/some.jpg',
                                 'google-com-path-to-some.jpg'
                             )
                         ])
def test_get_image_name_from_url(url, expected):
    assert get_image_name_from_url(url) == expected


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
def get_html_name_from_url(url, expected):
    assert get_html_name_from_url(url) == expected
