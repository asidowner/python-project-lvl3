import os.path
from shutil import rmtree

from urllib.parse import urlparse, urlunparse, ParseResult
from bs4 import BeautifulSoup
from requests import Session

from page_loader.lib.name_generator import get_file_name_from_url
from page_loader.lib.name_generator import get_file_dir_name_from_url
from page_loader.lib.name_generator import get_html_name_from_url

_ALLOWED_TAGS = ['img', 'link', 'script']


def save_site_from_bytes(req_session: Session,
                         output: str,
                         url: str) -> str:
    files_dir_name = get_file_dir_name_from_url(url)
    path_to_files_dir = os.path.join(output,
                                     files_dir_name)

    response = req_session.get(url)
    html: BeautifulSoup = _save_files(response.content,
                                      path_to_files_dir,
                                      url,
                                      req_session)

    file_name = get_html_name_from_url(url)
    file_path = os.path.join(output, file_name)

    with open(file_path, 'wb') as f:
        f.write(html.prettify(encoding='utf8'))

    return file_path


def _save_files(site_data: bytes,
                dir_path: str,
                url: str,
                req_session: Session) -> BeautifulSoup:
    html = BeautifulSoup(site_data, 'html.parser')

    parsed_url: ParseResult = urlparse(url)

    _make_files_dir(dir_path)

    files = html.find_all(_filter_tag)
    for index, file in enumerate(files):
        file_link = file['src']

        file_local_url = _save_file(parsed_url,
                                    file_link,
                                    dir_path,
                                    req_session)

        files[index] = _update_link_on_tag(file,
                                           file_local_url)

    return html


def _filter_tag(tag) -> bool:
    if tag.name in _ALLOWED_TAGS and tag.has_attr('src'):
        return True
    else:
        return False


def _update_link_on_tag(tag, value):
    tag['src'] = value
    return tag


def _make_files_dir(dir_path: str):
    if os.path.isdir(dir_path):
        rmtree(dir_path)
    os.mkdir(dir_path)


def _save_file(parsed_main_url: ParseResult,
               file_link: str,
               dir_path: str,
               req_session: Session) -> str:
    parsed_file_link = urlparse(file_link)
    if parsed_file_link.netloc != '':
        if parsed_file_link.netloc != parsed_main_url.netloc:
            return file_link

    file_url = urlunparse((parsed_main_url.scheme,
                           parsed_main_url.netloc,
                           parsed_file_link.path,
                           None,
                           None,
                           None))

    response = req_session.get(file_url)

    file_name = get_file_name_from_url(file_url)
    file_path = os.path.join(dir_path, file_name)
    with open(file_path, 'wb') as f:
        f.write(response.content)
    return '/'.join([os.path.basename(dir_path),
                     file_name])
