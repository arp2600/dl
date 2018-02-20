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


def filter_trash_contents(trash_path, trash_contents):
    pattern = re.compile('^\d+$')
    for item in trash_contents:
        if not pattern.match(item):
            continue

        full_path = os.path.join(trash_path, item)
        if not os.path.isdir(full_path):
            continue

        yield item


def main():
    if len(sys.argv) < 2:
        print("No arguments!")
        return

    # Filter out non-existent paths from  args
    args = sys.argv[1:]
    def check_arg(arg):
        if not os.path.exists(arg):
            print("Could not find {}".format(arg))
            return False
        return True

    args = [i for i in args if check_arg(i)]
    if not args:
        print("No valid arguments!")
        return

    # Check .trash exists
    home = os.path.expanduser('~')
    trash_path = os.path.join(home, '.trash')
    if not os.path.exists(trash_path):
        os.mkdir(trash_path)

    # User the contents of .trash to work out
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

    # Move items to trash folder
    trash_folder = os.path.join(trash_path, next_trash_folder)
    for source in args:
        # os.renames('some_dir/' ... raise an error
        # os.renames('some_dir' ...
        if source.endswith(os.sep):
            source = source[:-1]

        dest = os.path.join(trash_folder, source)
        print("Moving {} to {}".format(source, dest)) 
        os.renames(source, dest)


if __name__ == '__main__':
    main()
