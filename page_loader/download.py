from page_loader.downloader.site_downloader import save_site_from_bytes
from logging import getLogger

from requests import Session
import os

from page_loader.utils.exception import UnexpectedError
from page_loader.utils.exception import SiteNotAvailableError
from page_loader.utils.exception import FileNotAvailableError
from page_loader.utils.logging_tools import log_params

_CUR_DIR = os.getcwd()

_logger = getLogger()
_error_logger = getLogger('error')


@log_params(_logger)
def download(url: str,
             output: str = _CUR_DIR,
             req_session: Session = Session()) -> str:
    try:
        if not os.path.isdir(output):
            raise NotADirectoryError(f'Directory on {output}'
                                     f' not exists or not created')
        _logger.info(f'requested url: {url}')
        _logger.info(f'requested output: {output}')
        path_to_file = save_site_from_bytes(req_session,
                                            output,
                                            url)
        return path_to_file
    except (SiteNotAvailableError,
            FileNotAvailableError,
            NotADirectoryError,
            OSError) as e:
        _error_logger.error(e)
        raise
    except Exception as e:
        _error_logger.error(e)
        raise UnexpectedError('Unexpected error,'
                              ' try up logging level for more information')
