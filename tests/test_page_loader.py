import sys
import pytest

from page_loader.scripts.page_loader import main


def test_main(tmpdir,
              mock_session,
              main_html_url,
              expected_f_name,
              expected_html):
    sys.argv = ['page-loader', '--output', str(tmpdir), main_html_url]
    file_path = tmpdir.join(expected_f_name)
    with pytest.raises(SystemExit):
        main()
    with open(file_path, 'r', encoding='utf8') as f:
        assert f.read() == expected_html


def test_main_with_error(mock_session,
                         main_html_url,
                         expected_f_name,
                         expected_html):
    sys.argv = ['page-loader', '--output', 1, main_html_url]
    with pytest.raises(SystemExit):
        main()
