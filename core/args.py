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
    _parser.add_argument(
        '-o',
        '--output',
        default=None,
        help="Output NPF file, by default it replaces the given one",
    )
    _parser.add_argument(
        '--backup',
        default=None,
        help="If no -o/--output is given, this creates a backup, default is {npf}.bak",
    )
    _args = _parser.parse_args()
    _args.output = _args.output or _args.npf
    _args.backup = _args.backup or f"{_args.npf}.bak"


def get_args():
    global _args
    return _args


def get_parser():
    global _parser
    return _parser
