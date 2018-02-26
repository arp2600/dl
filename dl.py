#!/usr/bin/env python3
import argparse
import rm
import undo


def parse_args():
    parser = argparse.ArgumentParser(description='dl')
    parser.add_argument('file', nargs='*')
    parser.add_argument('-u', '--undo', action='store_true')
    return parser.parse_args(), parser


def main():
    args, parser = parse_args()
    if args.undo:
        undo.run(args)
    elif args.file:
        rm.run(args)
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
