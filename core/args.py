import argparse
import os
import sys

global _args
global _parser


def parse_args():
    global _args
    global _parser

    _parser = argparse.ArgumentParser(
        description="A checker that ensure the validity and conformance of an NPF",
    )
    _parser.add_argument(
        'npf',
        nargs='+',
    )
    _parser.add_argument(
        '-c',
        '--cache-dir',
        default=os.path.join(
            os.getcwd(),
            os.path.dirname(sys.argv[0]),
            'cache',
        ),
        help="Cache directory used to unpack and check the NPF. Default: cache/",
    )
    _args = _parser.parse_args()


def get_args():
    global _args
    return _args


def get_parser():
    global _parser
    return _parser
