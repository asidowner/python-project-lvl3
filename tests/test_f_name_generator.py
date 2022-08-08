from page_loader.lib.f_name_generator import get_f_name_from_url


def test_get_f_name_from_url_by_base_url():
    assert get_f_name_from_url('https://google.com') == 'google-com.html'


def test_get_f_name_from_url_with_qs():
    assert get_f_name_from_url('https://google.com?a=b') == 'google-com-a-b.html'


def test_get_f_name_from_url_with_path():
    assert get_f_name_from_url('https://google.com/path/to/some') == 'google-com-path-to-some.html'
