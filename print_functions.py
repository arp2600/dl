import sys
from termcolor import colored, cprint

def print_error(message):
    if sys.stderr.isatty():
        cprint(message, 'red', file=sys.stderr)
    else:
        print(message, file=sys.stderr)
