#!/usr/bin/env python3
import trash
from print_functions import print_verbose


def delete_path(path, verbosity):
    i = 1
    for item in path.glob('*'):
        i += 1
        i += delete_path(item, verbosity)

    if path.is_dir():
        print_verbose('rmdir {}'.format(path), verbosity, 2)
        path.rmdir()
    else:
        print_verbose('rm {}'.format(path), verbosity, 2)
        path.unlink()

    return i


def run(verbosity=0):
    trash_path = trash.get_trash_path()

    print_verbose('Emptying {}'.format(trash_path), verbosity, 1)
    print_verbose('', verbosity, 2)
    i = delete_path(trash_path, verbosity)
    print_verbose('', verbosity, 2)
    print_verbose('Removed {} items'.format(i), verbosity, 1)
