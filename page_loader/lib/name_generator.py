from urllib.parse import urlparse, ParseResult
from pathlib import PurePath
from logging import getLogger
import re
from page_loader.utils.logging_tools import log_params

_PATTERN = r'[\W|_]+'
_logger = getLogger('name_generator')


@log_params(_logger)
def _get_f_name_from_url(url: str) -> tuple:
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
    return file_name, suffix


@log_params(_logger)
def get_file_name_from_url(url: str):
    file_name, suffix = _get_f_name_from_url(url)
    result = ''.join([file_name, suffix])
    return result


@log_params(_logger)
def get_file_dir_name_from_url(url: str):
    file_name, suffix = _get_f_name_from_url(url)
    result = file_name + '_files'
    return result


@log_params(_logger)
def get_html_name_from_url(url: str):
    file_name, suffix = _get_f_name_from_url(url)
    result = ''.join([file_name, '.html'])
    return result


@log_params(_logger)
def _replace_by_regexp(value: str) -> str:
    result = re.sub(_PATTERN, '-', value)
    return result
