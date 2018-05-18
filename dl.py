#!/usr/bin/env python3
import argparse
import rm
import undo
import trash
import empty
from print_functions import Logger


def parse_args():
    parser = argparse.ArgumentParser(
        description='trash like program for command line')
    parser.add_argument('-v', '--verbose', action='count', default=0)

    subparsers = parser.add_subparsers(title='commands', dest='command')

    rm_parser = subparsers.add_parser(
        'rm', description='Delete files', help='Delete files')
    rm_parser.add_argument('file', nargs='+')

    # undo parser
    subparsers.add_parser(
        'undo',
        description='Undo the last rm command',
        help='Undo the last rm command')
    # size parser
    subparsers.add_parser(
        'size',
        description='Print the size of the trash directory',
        help='Print size of trash')
    # empty parser
    subparsers.add_parser(
        'empty',
        description='Empty the trash folder',
        help='Empty the trash folder')

    return parser.parse_args(), parser


def main():
    args, parser = parse_args()
    logger = Logger(args.verbose)

    switch = {
        'undo': lambda args: undo.run(logger),
        'size': lambda args: trash.print_size(args.verbose),
        'rm': lambda args: rm.run(args.file, logger),
        'empty': lambda args: empty.run(logger),
        None: lambda _: parser.print_help(),
    }
    switch[args.command](args)


if __name__ == '__main__':
    main()
