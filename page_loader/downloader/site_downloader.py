import os.path
from shutil import rmtree

from urllib.parse import urlparse, urlunparse, ParseResult
from bs4 import BeautifulSoup
from requests import Session

from page_loader.lib.name_generator import get_image_name_from_url
from page_loader.lib.name_generator import get_image_dir_name_from_url
from page_loader.lib.name_generator import get_html_name_from_url


def save_site_from_bytes(site_data: bytes,
                         output: str,
                         url: str,
                         req_session: Session) -> str:
    image_dir_name = get_image_dir_name_from_url(url)
    path_to_image_dir = os.path.join(output,
                                     image_dir_name)

    html: BeautifulSoup = _save_images(site_data,
                                       path_to_image_dir,
                                       url,
                                       req_session)
    file_name = get_html_name_from_url(url)
    file_path = os.path.join(output, file_name)

    with open(file_path, 'wb') as f:
        f.write(html.prettify(encoding='utf8'))

    return file_path


def _save_images(site_data: bytes,
                 dir_path: str,
                 url: str,
                 req_session: Session) -> BeautifulSoup:
    html = BeautifulSoup(site_data, 'html.parser')

    parsed_url: ParseResult = urlparse(url)

    _make_image_dir(dir_path)

    images = html.find_all('img')

    for index, image in enumerate(images):
        endpoint = image['src']

        image_local_url = _save_image(parsed_url,
                                      endpoint,
                                      dir_path,
                                      req_session)

        image['src'] = image_local_url
        images[index] = image

    return html


def _make_image_dir(dir_path: str):
    if os.path.isdir(dir_path):
        rmtree(dir_path)
    os.mkdir(dir_path)


def _save_image(parsed_url: ParseResult,
                endpoint: str,
                dir_path: str,
                req_session: Session) -> str:
    image_url = urlunparse((parsed_url.scheme,
                            parsed_url.netloc,
                            endpoint,
                            None,
                            None,
                            None))
    response = req_session.get(image_url)

    image_name = get_image_name_from_url(endpoint)
    image_path = os.path.join(dir_path, image_name)

    with open(image_path, 'wb') as f:
        f.write(response.content)

    return ''.join([os.path.basename(dir_path),
                    urlparse(image_url).path])
