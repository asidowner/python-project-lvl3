import os

import argparse
from page_loader.scripts.page_loader import main

class FakeParser:
    def __init__(self, *args, **kwargs):
        self.name_space = FakeNameSpace()

    def add_argument(self, *args, **kwargs):
        pass

    def parse_args(self, *args, **kwargs):
        return self.name_space


class FakeNameSpace:
    def __init__(self):
        self.url = 'https://google.com'
        self.output = os.getcwd()


def test_main():
    argparse.ArgumentParser = FakeParser
    main()
