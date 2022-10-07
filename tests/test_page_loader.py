import sys
import pytest

from page_loader.scripts.page_loader import main


def test_main(tmpdir,
              mock_session,
              main_html_url):
    sys.argv = ['page-loader', '--output', str(tmpdir), main_html_url]
    with pytest.raises(SystemExit):
        main()


def test_main_with_error(mock_session,
                         main_html_url):
    sys.argv = ['page-loader', '--output', 1, main_html_url]
    with pytest.raises(SystemExit):
        main()
