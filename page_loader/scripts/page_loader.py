#!/usr/bin/env python
import argparse
import os
import sys
from argparse import ArgumentParser, Namespace
from logging import getLogger

from page_loader import download

_MAIN_DESCRIPTION = 'Download html page and save to output directory'
_OUTPUT_DESCRIPTION = 'Path to output directory.' \
                      ' Should exists.' \
                      ' By default: current directory'
_URL_DESCRIPTION = 'URL to the page to be downloaded'

_logger = getLogger()


def main():
    try:
        args: Namespace = _get_command_args()
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


def _get_command_args() -> Namespace:
    parser: ArgumentParser = \
        argparse.ArgumentParser(description=_MAIN_DESCRIPTION)
    parser.add_argument('-o', '--output',
                        type=str,
                        help=_OUTPUT_DESCRIPTION, default=os.getcwd())
    parser.add_argument('url', type=str,
                        help=_URL_DESCRIPTION)
    return parser.parse_args()
