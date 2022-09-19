from logging import getLogger
from requests import Session, Timeout

from page_loader.utils.logging_tools import log_params
from page_loader.utils.exception import RequestUrlTimeoutError
from page_loader.utils.exception import GetSiteDataError

_logger = getLogger('utils')


@log_params(_logger)
def request_data(req_session: Session,
                 url: str) -> bytes or None:
    try:
        response = req_session.get(url)
    except Timeout:
        raise RequestUrlTimeoutError(f'Current url={url} '
                                     f'did not respond in'
                                     f' the allotted time')

    if response.status_code != 200:
        raise GetSiteDataError(f'Site return'
                               f' HTTP code = {response.status_code}'
                               f' on this resources: {url}')

    return response.content
