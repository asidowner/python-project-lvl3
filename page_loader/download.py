from page_loader.downloader.site_downloader import save_site_from_bytes
from logging import getLogger

import os

from page_loader.utils.exception import UnexpectedError, \
    GetSiteDataError, \
    SaveMainFileError, \
    SaveAdditionalFileError, \
    RequestUrlTimeoutError, \
    DeleteDirForFilesError, \
    CreateDirForFilesError

from page_loader.utils.logging_tools import log_params

_CUR_DIR = os.getcwd()

_logger = getLogger()
_error_logger = getLogger('error')


@log_params(_logger)
def download(url: str,
             output: str = _CUR_DIR) -> str:
    _logger.info(f'requested url: {url}')
    _logger.info(f'requested output: {output}')

    try:
        if not os.path.isdir(output):
            raise NotADirectoryError(f'Directory on {output}'
                                     f' not exists or not created')

        _logger.info('Start save HTML')

        path_to_file = save_site_from_bytes(output,
                                            url)

        _logger.info('Site data saved successfully')
        return path_to_file
    except (GetSiteDataError,
            NotADirectoryError,
            SaveMainFileError,
            SaveAdditionalFileError,
            RequestUrlTimeoutError,
            DeleteDirForFilesError,
            CreateDirForFilesError
            ) as e:
        _error_logger.error(e)
        raise
    except Exception as e:
        _error_logger.error(e)
        raise UnexpectedError('Unexpected error,'
                              ' try up logging level for more information')
