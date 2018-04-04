import sys
from termcolor import colored, cprint

def print_error(message):
    cprint(message, 'red', file=sys.stderr)
