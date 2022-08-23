from page_loader.downloader.site_downloader import save_site_from_bytes

from requests import Session
import os

_CUR_DIR = os.getcwd()


def download(url: str,
             output: str = _CUR_DIR,
             req_session: Session = Session()) -> str:
    if not os.path.isdir(output):
        raise NotADirectoryError(f'Directory on {output}'
                                 f' not exists or not created')

    response = req_session.get(url)

    path_to_file = save_site_from_bytes(response.content,
                                        output,
                                        url,
                                        req_session)

    return path_to_file
