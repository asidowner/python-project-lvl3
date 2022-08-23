from urllib.parse import urlparse, ParseResult
from pathlib import PurePath
import re

_PATTERN = r'\W'


def _get_f_name_from_url(url: str) -> tuple:
    url_parsed: ParseResult = urlparse(url)
    file_name_parts: list = [url_parsed.netloc]
    suffix: str = ''

    # If path exists find suffix and replace
    if url_parsed.path:
        suffix: str = PurePath(url_parsed.path).suffix
        url_path: str = url_parsed.path.replace(suffix, '')
        file_name_parts.append(url_path)

    if url_parsed.query:
        file_name_parts.append('-' + url_parsed.query)

    file_name: str = ''.join(list(map(_replace_by_regexp, file_name_parts)))

    return file_name, suffix


def get_image_name_from_url(url: str):
    file_name, suffix = _get_f_name_from_url(url)
    return ''.join([file_name, suffix])


def get_image_dir_name_from_url(url: str):
    file_name, suffix = _get_f_name_from_url(url)
    return file_name + '_files'


def get_html_name_from_url(url: str):
    file_name, suffix = _get_f_name_from_url(url)
    return ''.join([file_name, '.html'])


def _replace_by_regexp(value: str) -> str:
    return re.sub(_PATTERN, '-', value)
