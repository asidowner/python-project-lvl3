import logging.config
import os

_LOGGING_LEVEL = os.environ.get('PAGE_LOADER_LOGGING_LEVEL')
_AVAILABLE_LOGGING_LEVEL = ('DEBUG',
                            'INFO',
                            'WARNING',
                            'ERROR',
                            'CRITICAL',
                            'NOTSET')

if not _LOGGING_LEVEL or _LOGGING_LEVEL not in _AVAILABLE_LOGGING_LEVEL:
    _LOGGING_LEVEL = 'INFO'

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
    },
    'loggers': {
        '': {  # root logger
            'handlers': ['default'],
            'level': 'NOTSET',
            'qualname': 'root',
            'propagate': True
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
