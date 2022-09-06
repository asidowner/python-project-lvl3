from page_loader.downloader.site_downloader import save_site_from_bytes
from logging import getLogger

from requests import Session
import os

_CUR_DIR = os.getcwd()

_logger = getLogger()


def download(url: str,
             output: str = _CUR_DIR,
             req_session: Session = Session()) -> str:
    _logger.debug('Start download')
    _logger.debug(f'output: {url}')
    _logger.debug(f'output: {output}')
    try:
        if not os.path.isdir(output):
            raise NotADirectoryError(f'Directory on {output}'
                                     f' not exists or not created')

        path_to_file = save_site_from_bytes(req_session,
                                            output,
                                            url)
        _logger.debug(f'path_to_file: {path_to_file}')
        return path_to_file
    except Exception as e:
        _logger.error(f'{e}')
        raise
