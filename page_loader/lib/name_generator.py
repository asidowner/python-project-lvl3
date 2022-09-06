from urllib.parse import urlparse, ParseResult
from pathlib import PurePath
from logging import getLogger
import re

_PATTERN = r'[\W|_]+'
_logger = getLogger('name_generator')


def _get_f_name_from_url(url: str) -> tuple:
    _logger.debug('Start _get_f_name_from_url')
    _logger.debug(f'url: {url}')

    url_parsed: ParseResult = urlparse(url)
    _logger.debug(f'url_parsed: {url_parsed}')

    file_name_parts: list = [url_parsed.netloc]
    _logger.debug(f'file_name_parts: {file_name_parts}')

    suffix: str = ''

    # If path exists find suffix and replace
    if url_parsed.path:
        _logger.debug('If url_parsed branch')

        suffix: str = PurePath(url_parsed.path).suffix
        _logger.debug(f'suffix: {suffix}')

        url_path: str = url_parsed.path.replace(suffix, '')
        _logger.debug(f'url_path: {url_path}')

        file_name_parts.append(url_path)
        _logger.debug(f'file_name_parts: {file_name_parts}')

    if url_parsed.query:
        file_name_parts.append('-' + url_parsed.query)
        _logger.debug(f'file_name_parts: {file_name_parts}')

    file_name: str = ''.join(list(map(_replace_by_regexp, file_name_parts)))
    _logger.debug(f'file_name: {file_name}')
    _logger.debug(f'suffix: {suffix}')

    _logger.debug('End _get_f_name_from_url')
    return file_name, suffix


def get_file_name_from_url(url: str):
    _logger.debug('Start get_file_name_from_url')
    file_name, suffix = _get_f_name_from_url(url)

    result = ''.join([file_name, suffix])
    _logger.debug(f'result: {result}')

    _logger.debug('End get_file_name_from_url')
    return result


def get_file_dir_name_from_url(url: str):
    _logger.debug('Start get_file_dir_name_from_url')
    file_name, suffix = _get_f_name_from_url(url)

    result = file_name + '_files'
    _logger.debug(f'result: {result}')

    _logger.debug('End get_file_dir_name_from_url')
    return result


def get_html_name_from_url(url: str):
    _logger.debug('Start get_html_name_from_url')
    file_name, suffix = _get_f_name_from_url(url)

    result = ''.join([file_name, '.html'])
    _logger.debug(f'result: {result}')

    _logger.debug('End get_html_name_from_url')
    return result


def _replace_by_regexp(value: str) -> str:
    _logger.debug('Start _replace_by_regexp')
    _logger.debug(f'value: {value}')

    result = re.sub(_PATTERN, '-', value)

    _logger.debug(f'result: {result}')
    _logger.debug('End _replace_by_regexp')

    return result
