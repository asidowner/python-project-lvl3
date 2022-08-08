from requests import Session
import os
from page_loader.lib.f_name_generator import get_f_name_from_url

_CUR_DIR = os.getcwd()


def download(url: str,
             output: str = _CUR_DIR,
             req_session: Session = Session()) -> str:
    if not os.path.isdir(output):
        raise NotADirectoryError(f'Directory on {output}'
                                 f' not exists or not created')

    response = req_session.get(url)
    path_to_file = os.path.join(output, get_f_name_from_url(url))

    with open(path_to_file, 'w') as f:
        f.write(response.text)

    return path_to_file
