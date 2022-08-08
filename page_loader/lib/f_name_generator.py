from urllib.parse import urlparse
from pathlib import PurePath
import re

PATTERN = r'\W'


def get_f_name_from_url(url: str) -> str:
    url_parsed = urlparse(url)

    file_name_parts = [url_parsed.netloc]

    # If path exists find suffix and replace
    if url_parsed.path:
        suffix = PurePath(url_parsed.path).suffix
        file_name_parts.append(url_parsed.path.replace(suffix, ''))

    if url_parsed.query:
        file_name_parts.append('-' + url_parsed.query)

    file_name = ''.join(list(map(_replace_by_regexp, file_name_parts)))

    return file_name + '.html'


def _replace_by_regexp(value: str) -> str:
    return re.sub(PATTERN, '-', value)
