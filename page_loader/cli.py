import argparse
import os

from argparse import ArgumentParser, Namespace

_MAIN_DESCRIPTION = 'Download html page and save to output directory'
_OUTPUT_DESCRIPTION = 'Path to output directory.' \
                      ' Should exists.' \
                      ' By default: current directory'
_URL_DESCRIPTION = 'URL to the page to be downloaded'


def get_command_args() -> Namespace:
    parser: ArgumentParser = \
        argparse.ArgumentParser(description=_MAIN_DESCRIPTION)
    parser.add_argument('-o', '--output',
                        type=str,
                        help=_OUTPUT_DESCRIPTION, default=os.getcwd())
    parser.add_argument('url', type=str,
                        help=_URL_DESCRIPTION)
    return parser.parse_args()
