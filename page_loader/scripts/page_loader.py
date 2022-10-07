#!/usr/bin/env python
import sys
from argparse import Namespace
from logging import getLogger

from page_loader import download
from page_loader.cli import get_command_args

_logger = getLogger()


def main():
    try:
        _logger.info(sys.argv)
        _logger.info(sys.orig_argv)
        args: Namespace = get_command_args()
        _logger.info('Start app')
        _logger.debug(f'url={args.url}')
        _logger.debug(f'output={args.output}')

        file_path = download(
            args.url,
            args.output
        )

        print(f'\nPage was downloaded as {file_path}')
        sys.exit()
    except Exception as e:
        sys.exit(e)
