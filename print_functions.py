import sys
from termcolor import cprint


class Logger:
    def __init__(self, verbosity=0):
        self.verbosity = verbosity

    def print(self, message, minimum_verbosity):
        if self.verbosity >= minimum_verbosity:
            print(message)

    def error(self, message):
        if sys.stderr.isatty():
            cprint(message, 'red', file=sys.stderr)
        else:
            print(message, file=sys.stderr)

    def print_move(self, source, dest):
        if self.verbosity == 1:
            print(source)
        elif self.verbosity > 1:
            print("{} -> {}".format(source, dest))
