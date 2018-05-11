import sys
from termcolor import colored, cprint


def print_verbose(message, verbosity, minimum):
    if verbosity >= minimum:
        print(message)


def print_error(message):
    if sys.stderr.isatty():
        cprint(message, 'red', file=sys.stderr)
    else:
        print(message, file=sys.stderr)


def print_move(source, dest, verbosity):
    if verbosity == 1:
        print(source)
    elif verbosity > 1:
        print("{} -> {}".format(source, dest))
