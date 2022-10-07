import os
import stat
import pytest

from page_loader.downloader.files_downloader import _make_files_dir
from page_loader.downloader.files_downloader import _save_file
from page_loader.lib.name_generator import get_file_dir_name_from_url
from page_loader.utils.exception import DeleteDirForFilesError
from page_loader.utils.exception import CreateDirForFilesError
from page_loader.utils.exception import SaveAdditionalFileError


def test_make_files_dir_create_error(tmpdir, main_html_url):
    dir_path = tmpdir.join('tmp')
    if not os.path.exists('tmp'):
        os.mkdir(dir_path, stat.S_IREAD)
    with pytest.raises(CreateDirForFilesError):
        _make_files_dir(dir_path, main_html_url)
    os.rmdir(dir_path)


def test_make_files_dir_delete_error(tmpdir, main_html_url):
    dir_name = get_file_dir_name_from_url(main_html_url)
    dir_path = os.path.join(tmpdir, 'tmp')
    files_dir_path = os.path.join(dir_path, dir_name)
    if not os.path.exists(dir_path):
        os.mkdir(dir_path)
    if not os.path.exists(files_dir_path):
        os.mkdir(files_dir_path, stat.S_ISVTX)
    with pytest.raises(DeleteDirForFilesError):
        _make_files_dir(dir_path, main_html_url)
    os.rmdir(files_dir_path)
    os.rmdir(dir_path)


def test__save_file(tmpdir, main_html_url, html_url_to_image, mock_session):
    dir_path = tmpdir.join('tmp')
    if not os.path.exists('tmp'):
        os.mkdir(dir_path, stat.S_IREAD)
    with pytest.raises(SaveAdditionalFileError):
        _save_file(main_html_url, html_url_to_image, dir_path)
    os.rmdir(dir_path)
