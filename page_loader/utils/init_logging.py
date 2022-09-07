import logging.config
import os

_LOGGING_LEVEL = os.environ.get('PAGE_LOADER_LOGGING_LEVEL', 'INFO')

_LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'standard': {
            'format': '%(asctime)s %(name)s %(levelname)s %(message)s'
        },
    },
    'handlers': {
        'default': {
            'level': _LOGGING_LEVEL,
            'formatter': 'standard',
            'class': 'logging.StreamHandler',
            'stream': 'ext://sys.stdout'
        },
        'error': {
            'level': 'ERROR',
            'formatter': 'standard',
            'class': 'logging.StreamHandler',
            'stream': 'ext://sys.stderr'
        },
    },
    'loggers': {
        '': {  # root logger
            'handlers': ['default'],
            'level': 'NOTSET',
            'qualname': 'root',
            'propagate': True
        },
        'error': {
            'handlers': ['default'],
            'level': 'ERROR',
            'qualname': 'error',
            'propagate': False
        },
        'downloader': {
            'handlers': ['default'],
            'level': _LOGGING_LEVEL,
            'qualname': 'downloader',
            'propagate': False
        },
        'name_generator': {
            'handlers': ['default'],
            'level': _LOGGING_LEVEL,
            'qualname': 'name_generator',
            'propagate': False
        },
        '__main__': {  # if __name__ == '__main__'
            'handlers': ['default'],
            'level': _LOGGING_LEVEL,
            'propagate': False
        },
    }
}


def init_logging():
    logging.config.dictConfig(_LOGGING_CONFIG)
