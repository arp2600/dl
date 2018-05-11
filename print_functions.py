import sys
from termcolor import colored, cprint


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


class Logger:
    def __init__(self, verbosity=0):
        self.verbosity = verbosity

    def print(self, message, minimum_verbosity):
        if self.verbosity >= minimum_verbosity:
            print(message)
