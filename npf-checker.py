#!/usr/bin/env python3

import core.args
import core.package


def main():
    core.args.parse_args()
    args = core.args.get_args()
    for f in args.npf:
        pkg = core.package.Package(f)
        pkg.unwrap()


if __name__ == '__main__':
    main()
