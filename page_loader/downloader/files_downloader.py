import os
from logging import Logger, getLogger
from shutil import rmtree
from urllib.parse import ParseResult, urlparse, urlunparse

from requests import Session
from bs4 import BeautifulSoup

from progress.bar import IncrementalBar

from page_loader.lib.name_generator import get_file_dir_name_from_url
from page_loader.lib.name_generator import get_file_name_from_url
from page_loader.utils.exception import SaveAdditionalFileError
from page_loader.utils.logging_tools import log_params
from page_loader.utils.progress_bar import get_progress_bar
from page_loader.utils.request_tools import request_data

_logger: Logger = getLogger('downloader')

_progress_bar: IncrementalBar = get_progress_bar()


@log_params(_logger)
def save_files(site_data: bytes,
               output_path: str,
               url: str,
               req_session: Session) -> BeautifulSoup:
    html = BeautifulSoup(site_data, 'html.parser')

    path_to_files_dir = _make_files_dir(output_path, url)

    files = html.find_all(_filter_tag)

    progress_interest = 100 / len(files) + 1
    _progress_bar.next(int(progress_interest))

    for index, file in enumerate(files):
        file_link = _get_url(file)

        file_local_url = _save_file(url,
                                    file_link,
                                    path_to_files_dir,
                                    req_session)

        files[index] = _update_link_on_tag(file,
                                           file_local_url)
        _progress_bar.next(int(progress_interest))
    return html


@log_params(_logger)
def _save_file(main_url: str,
               file_link: str,
               dir_path: str,
               req_session: Session) -> str:
    parsed_main_url = urlparse(main_url)
    parsed_file_link = urlparse(file_link)

    if parsed_file_link.netloc != '':
        if parsed_file_link.netloc != parsed_main_url.netloc:
            return file_link

    file_url = _get_file_url(parsed_main_url,
                             parsed_file_link)

    _logger.debug(f'file_url: {file_url}')

    resp_content = request_data(req_session, file_url)

    file_name = get_file_name_from_url(file_url)
    file_path = os.path.join(dir_path, file_name)

    try:
        with open(file_path, 'wb') as f:
            f.write(resp_content)
    except OSError:
        raise SaveAdditionalFileError(f"Can't write data"
                                      f" to {file_path},"
                                      f" check permissions")

    result = '/'.join([os.path.basename(dir_path),
                       file_name])
    return result


@log_params(_logger)
def _get_file_url(parsed_main_url: ParseResult,
                  parsed_file_link: ParseResult) -> str:
    return urlunparse((parsed_main_url.scheme,
                       parsed_main_url.netloc,
                       parsed_file_link.path,
                       None,
                       None,
                       None))


@log_params(_logger)
def _filter_tag(tag) -> bool:
    if tag.name in ('script', 'img') and tag.has_attr('src'):
        return True
    elif tag.name == 'link':
        return True
    else:
        return False


@log_params(_logger)
def _get_url(tag) -> str:
    return tag.get('href', tag.get('src'))


@log_params(_logger)
def _update_link_on_tag(tag, value):
    if tag.get('src'):
        tag['src'] = value
    else:
        tag['href'] = value
    return tag


@log_params(_logger)
def _make_files_dir(output_path: str,
                    url: str):
    files_dir_name = get_file_dir_name_from_url(url)
    path_to_files_dir = os.path.join(output_path,
                                     files_dir_name)
    if os.path.isdir(path_to_files_dir):
        _logger.debug('Dir for additional files exists, try delete')
        rmtree(path_to_files_dir)
    os.mkdir(path_to_files_dir)
    return path_to_files_dir
