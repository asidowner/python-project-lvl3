import os.path

from logging import getLogger, Logger
from bs4 import BeautifulSoup
from requests import Session

from page_loader.downloader.files_downloader import save_files
from page_loader.lib.name_generator import get_html_name_from_url
from page_loader.utils.exception import SaveMainFileError
from page_loader.utils.logging_tools import log_params
from page_loader.utils.request_tools import request_data

_logger: Logger = getLogger('downloader')


@log_params(_logger)
def save_site_from_bytes(req_session: Session,
                         output_path: str,
                         url: str) -> str:
    site_name = get_html_name_from_url(url)
    site_path = os.path.join(output_path, site_name)

    _logger.info(f'write html file: {site_path}')

    resp_content = request_data(req_session, url)
    _logger.info('Site data received successfully')

    html: BeautifulSoup = save_files(resp_content,
                                     output_path,
                                     url,
                                     req_session)

    try:
        with open(site_path, 'w') as f:
            f.write(html.prettify())
    except OSError:
        raise SaveMainFileError(f"Can't write data"
                                f' to {site_path}, check permissions')

    return site_path
