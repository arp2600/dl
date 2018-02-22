#!/usr/bin/env python3
import re
import sys
import base64
from pathlib import Path

# Load state
#   Check .Trash folder exists
#   Count numbered folders in .Trash
# Create new folder in .Trash
# Move arg items to new folder in .Trash


def build_subparser(parser):
    parser.add_argument('file', nargs='+')


# Filter out non-existent paths from  args
def read_and_check_paths(paths):
    def check_path(path):
        if not path.exists():
            print("Could not find {}".format(path))
            return False
        return True

    paths = (Path(i) for i in paths)
    paths = [i for i in paths if check_path(i)]
    if not paths:
        print("No valid file paths!")
        sys.exit(1)

    return paths


def check_or_create_trash():
    home = Path.home()
    trash_path = home / '.dl' / 'trash'
    if not trash_path.exists():
        trash_path.mkdir(parents=True)

    return trash_path


def get_trash_folder():
    trash_path = check_or_create_trash()

    # User the contents of trash to work out
    # the number for the next trash folder
    pattern = re.compile('^\d+$')
    condition = lambda x: x.is_dir and pattern.match(x.name)
    trash_contents = [x for x in trash_path.iterdir() if condition(x)]

    if trash_contents:
        next_trash_folder = max([int(i.name) for i in trash_contents]) + 1
        next_trash_folder = str(next_trash_folder)
    else:
        next_trash_folder = '0'

    trash_folder = trash_path / next_trash_folder
    trash_folder.mkdir()

    return trash_folder


def hash_path(path):
    path = str.encode(str(path))
    return base64.b64encode(path).decode('utf-8')


def move_to_trash(source, trash_folder):
    t = Path(trash_folder)
    if source.is_absolute():
        hsh = hash_path(source)[:8]
        dest = t / hsh / source.name
    else:
        dest = t / source

    print("Moving {} to {}".format(source, dest))
    if not dest.parent.exists():
        dest.parent.mkdir(parents=True)
    source.rename(dest)


def run(args):
    # Call filter paths first. In the event of none of the
    # paths being valid, get_trash_folder wont create a new folder
    paths = read_and_check_paths(args.file)
    trash_folder = get_trash_folder()

    # Move items to trash folder
    for source in paths:
        move_to_trash(source, trash_folder)


if __name__ == '__main__':
    main()
