import os
from logging import Logger, getLogger
from shutil import rmtree
from urllib.parse import ParseResult, urlparse, urlunparse

from requests import Session
from bs4 import BeautifulSoup

from progress.bar import IncrementalBar

from page_loader.lib.name_generator import get_file_dir_name_from_url
from page_loader.lib.name_generator import get_file_name_from_url
from page_loader.utils.exception import FileNotAvailableError
from page_loader.utils.logging_tools import log_params
from page_loader.utils.progress_bar import get_progress_bar

_logger: Logger = getLogger('downloader')

_progress_bar: IncrementalBar = get_progress_bar()


@log_params(_logger)
def save_files(site_data: bytes,
               output_path: str,
               url: str,
               req_session: Session) -> BeautifulSoup:
    html = BeautifulSoup(site_data)

    parsed_url: ParseResult = urlparse(url)
    _logger.debug(f'url: {parsed_url}')

    files_dir_name = get_file_dir_name_from_url(url)
    path_to_files_dir = os.path.join(output_path,
                                     files_dir_name)

    _logger.debug(f'path_to_files_dir={path_to_files_dir}')
    _make_files_dir(path_to_files_dir)

    files = html.find_all(_filter_tag)
    progress_interest = 100 / len(files) + 1
    _progress_bar.next(int(progress_interest))
    for index, file in enumerate(files):
        file_link = _get_url(file)
        _logger.debug(f'file_link: {file_link}')

        file_local_url = _save_file(parsed_url,
                                    file_link,
                                    path_to_files_dir,
                                    req_session)
        _logger.debug(f'file_local_url: {file_local_url}')

        files[index] = _update_link_on_tag(file,
                                           file_local_url)
        _progress_bar.next(int(progress_interest))
    return html


@log_params(_logger)
def _save_file(parsed_main_url: ParseResult,
               file_link: str,
               dir_path: str,
               req_session: Session) -> str:
    parsed_file_link = urlparse(file_link)

    _logger.debug(f'parsed_file_link: {parsed_file_link}')

    if parsed_file_link.netloc != '':
        if parsed_file_link.netloc != parsed_main_url.netloc:
            return file_link

    file_url = urlunparse((parsed_main_url.scheme,
                           parsed_main_url.netloc,
                           parsed_file_link.path,
                           None,
                           None,
                           None))

    _logger.debug(f'file_url: {file_url}')

    response = req_session.get(file_url)
    if response.status_code != 200:
        raise FileNotAvailableError(f'Site return'
                                    f' HTTP code = {response.status_code}'
                                    f' on this resources: {file_url}')

    file_name = get_file_name_from_url(file_url)
    file_path = os.path.join(dir_path, file_name)

    _logger.debug(f'file_path: {file_path}')

    try:
        with open(file_path, 'wb') as f:
            f.write(response.content)
    except OSError:
        _logger.error(f"Can't write data to {file_path}, check permissions")
        raise

    result = '/'.join([os.path.basename(dir_path),
                       file_name])
    return result


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
def _make_files_dir(dir_path: str):
    if os.path.isdir(dir_path):
        _logger.debug('Dir for additional files exists, try delete')
        rmtree(dir_path)
    os.mkdir(dir_path)
