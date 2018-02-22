#!/usr/bin/env python3
import argparse
import rm
import undo


def parse_args():
    parser = argparse.ArgumentParser(description='dl')
    subparsers = parser.add_subparsers(dest='command')
    rm.build_subparser(subparsers.add_parser('rm'))
    undo.build_subparser(subparsers.add_parser('undo'))
    return parser.parse_args()


def main():
    args = parse_args()
    if args.command == 'rm':
        rm.run(args)
    elif args.command == 'undo':
        undo.run(args)


if __name__ == '__main__':
    main()
