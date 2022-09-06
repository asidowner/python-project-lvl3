import os.path
from shutil import rmtree

from logging import getLogger
from urllib.parse import urlparse, urlunparse, ParseResult
from bs4 import BeautifulSoup
from requests import Session

from page_loader.lib.name_generator import get_file_name_from_url
from page_loader.lib.name_generator import get_file_dir_name_from_url
from page_loader.lib.name_generator import get_html_name_from_url
from page_loader.utils.exception import SiteNotAvailableError

_ALLOWED_TAGS = ['img', 'link', 'script']

_logger = getLogger('downloader')


def save_site_from_bytes(req_session: Session,
                         output_path: str,
                         url: str) -> str:
    _logger.debug('Start save_site_from_bytes')
    _logger.debug(f'output: {output_path}')
    _logger.debug(f'url: {url}')

    _logger.info('Try to get site data')

    _logger.debug(f'Request {url}')
    response = req_session.get(url)

    if response.status_code != 200:
        _logger.error(f'GET {url} return:'
                      f'\nstatus_code {response.status_code}'
                      f'\nresponse: {response.text}')
        raise SiteNotAvailableError('Site return HTTP'
                                    ' status_code != 200')

    _logger.info('Site data received successfully')
    _logger.debug(f'status_code: {response.status_code}')
    _logger.debug(f'response: {response.text}')

    files_dir_name = get_file_dir_name_from_url(url)
    path_to_files_dir = os.path.join(output_path,
                                     files_dir_name)

    _logger.debug(f'files_dir_name: {files_dir_name}')
    _logger.debug(f'path_to_files_dir: {path_to_files_dir}')

    html: BeautifulSoup = _save_files(response.content,
                                      path_to_files_dir,
                                      url,
                                      req_session)

    _logger.debug(f'path_to_files_dir: {path_to_files_dir}')

    file_name = get_html_name_from_url(url)
    file_path = os.path.join(output_path, file_name)

    _logger.debug(f'file_name: {file_name}')
    _logger.debug(f'file_path: {file_path}')

    with open(file_path, 'wb') as f:
        f.write(html.prettify(encoding='utf8'))
    _logger.info('Site data saved')

    _logger.debug('End save_site_from_bytes')
    return file_path


def _save_files(site_data: bytes,
                dir_path: str,
                url: str,
                req_session: Session) -> BeautifulSoup:
    _logger.debug('Start _save_files')
    _logger.debug(f'site_data: {site_data}')
    _logger.debug(f'dir_path: {dir_path}')
    _logger.debug(f'url: {url}')

    html = BeautifulSoup(site_data, 'html.parser')

    parsed_url: ParseResult = urlparse(url)
    _logger.debug(f'url: {parsed_url}')

    _make_files_dir(dir_path)

    files = html.find_all(_filter_tag)
    for index, file in enumerate(files):
        file_link = file['src']
        _logger.debug(f'file_link: {file_link}')

        file_local_url = _save_file(parsed_url,
                                    file_link,
                                    dir_path,
                                    req_session)
        _logger.debug(f'file_local_url: {file_local_url}')

        files[index] = _update_link_on_tag(file,
                                           file_local_url)

    _logger.debug('End _save_files')
    return html


def _filter_tag(tag) -> bool:
    _logger.debug('Start _filter_tag')
    _logger.debug(f'tag: {tag}')
    if tag.name in _ALLOWED_TAGS and tag.has_attr('src'):
        _logger.debug('End _filter_tag with True result')
        return True
    else:
        _logger.debug('End _filter_tag with False result')
        return False


def _update_link_on_tag(tag, value):
    _logger.debug('Start _update_link_on_tag')
    _logger.debug(f'tag: {tag}')
    _logger.debug(f'value: {value}')
    tag['src'] = value
    _logger.debug(f'tag after update: {tag}')
    _logger.debug('End _update_link_on_tag')
    return tag


def _make_files_dir(dir_path: str):
    _logger.debug('Start _make_files_dir')
    _logger.debug(f'dir_path: {dir_path}')
    if os.path.isdir(dir_path):
        _logger.debug('Dir for additional files exists, try delete')
        rmtree(dir_path)
    os.mkdir(dir_path)
    _logger.debug('End _make_files_dir')


def _save_file(parsed_main_url: ParseResult,
               file_link: str,
               dir_path: str,
               req_session: Session) -> str:
    _logger.debug('Start _save_file')
    _logger.debug(f'parsed_main_url: {parsed_main_url}')
    _logger.debug(f'file_link: {file_link}')
    _logger.debug(f'dir_path: {dir_path}')

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

    _logger.info('Try get additional file')
    response = req_session.get(file_url)
    if response.status_code != 200:
        _logger.error(f'GET {file_url} return:'
                      f'\nstatus_code {response.status_code}'
                      f'\nresponse: {response.text}')
        raise SiteNotAvailableError('Url to file return HTTP'
                                    ' status_code != 200')

    file_name = get_file_name_from_url(file_url)
    file_path = os.path.join(dir_path, file_name)

    _logger.debug(f'file_name: {file_name}')
    _logger.debug(f'file_path: {file_path}')

    with open(file_path, 'wb') as f:
        f.write(response.content)
    _logger.info('Additional file saved')

    result = '/'.join([os.path.basename(dir_path),
                       file_name])
    _logger.debug(f'result: {result}')
    _logger.debug('End _save_file')
    return result
