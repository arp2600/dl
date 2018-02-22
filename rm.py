#!/usr/bin/env python3
import re
import os
import os.path
import sys

# Load state
#   Check .Trash folder exists
#   Count numbered folders in .Trash
# Create new folder in .Trash
# Move arg items to new folder in .Trash


def build_subparser(parser):
    parser.add_argument('file', nargs='+')


def filter_trash_contents(trash_path, trash_contents):
    pattern = re.compile('^\d+$')
    for item in trash_contents:
        if not pattern.match(item):
            continue

        full_path = os.path.join(trash_path, item)
        if not os.path.isdir(full_path):
            continue

        yield item


# Filter out non-existent paths from  args
def filter_paths(paths):
    def check_path(path):
        if not os.path.exists(path):
            print("Could not find {}".format(path))
            return False
        return True

    paths = [i for i in paths if check_path(i)]
    if not paths:
        print("No valid file paths!")
        sys.exit(1)

    return paths


def check_or_create_trash():
    home = os.path.expanduser('~')
    trash_path = os.path.join(home, '.dl/trash')
    if not os.path.exists(trash_path):
        os.makedirs(trash_path)

    return trash_path


def get_trash_folder():
    trash_path = check_or_create_trash()

    # User the contents of trash to work out
    # the number for the next trash folder
    trash_contents = os.listdir(trash_path)
    trash_contents = [
        i for i in filter_trash_contents(trash_path, trash_contents)
    ]

    if trash_contents:
        next_trash_folder = max([int(i) for i in trash_contents]) + 1
        next_trash_folder = str(next_trash_folder)
    else:
        next_trash_folder = '0'

    os.mkdir(os.path.join(trash_path, next_trash_folder))

    trash_folder = os.path.join(trash_path, next_trash_folder)
    return trash_folder


def move_to_trash(source, trash_folder):
    # os.renames('some_dir/' ... raise an error
    # os.renames('some_dir' ...
    if source.endswith(os.sep):
        source = source[:-1]

    # Leading slash on absolute paths needs to be removed
    # os.path.join('some_dir', '/absolute/path')
    # will return '/absolute/path'
    dest = source
    if dest.startswith(os.sep):
        dest = dest[1:]
    dest = os.path.join(trash_folder, dest)

    print("Moving {} to {}".format(source, dest))
    os.renames(source, dest)


def run(args):
    # Call filter paths first. In the event of none of the
    # paths being valid, get_trash_folder wont create a new folder
    paths = filter_paths(args.file)
    trash_folder = get_trash_folder()

    # Move items to trash folder
    for source in paths:
        move_to_trash(source, trash_folder)


if __name__ == '__main__':
    main()
