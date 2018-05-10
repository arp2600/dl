#!/usr/bin/env python3
import argparse
import rm
import undo
import trash


def parse_args():
    parser = argparse.ArgumentParser(description='dl')
    parser.add_argument('file', nargs='*')
    parser.add_argument('-u', '--undo', action='store_true')
    parser.add_argument('-s', '--size', action='store_true')
    parser.add_argument('-v', '--verbose', action='count', default=0)
    return parser.parse_args(), parser


def main():
    args, parser = parse_args()
    if args.undo:
        undo.run(args.verbose)
    elif args.size:
        trash.print_size(args.verbose)
    elif args.file:
        rm.run(args.file, args.verbose)
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
