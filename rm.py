#!/usr/bin/env python3
import sys
import base64
import pickle
import trash
from pathlib import Path


# Load state
#   Check .Trash folder exists
#   Count numbered folders in .Trash
# Create new folder in .Trash
# Move arg items to new folder in .Trash
class Info:
    def __init__(self):
        self.moves = []

    def add_move(self, source, dest):
        self.moves.append((source, dest))

    def __str__(self):
        out = ["rm.Info:"]
        for source, dest in self.moves:
            out.append('  {} => {}'.format(source, dest))

        return '\n'.join(out)


# Filter out non-existent paths from  args
def read_and_check_paths(paths, logger):
    def check_path(path):
        if not path.exists():
            logger.error("Could not find {}".format(path))
            return False
        return True

    paths = (Path(i) for i in paths)
    paths = [i for i in paths if check_path(i)]
    if not paths:
        logger.error("No valid file paths!")
        sys.exit(1)

    return paths


def hash_path(path):
    path = str.encode(str(path))
    return base64.b64encode(path).decode('utf-8')


def move_to_trash(source, trash_folder, logger):
    t = Path(trash_folder)
    if source.is_absolute():
        hsh = hash_path(source)[:8]
        dest = t / hsh / source.name
    else:
        dest = t / source

    logger.print_move(source, dest)
    if not dest.parent.exists():
        dest.parent.mkdir(parents=True)
    source.rename(dest)
    return dest


def run(files, logger):
    # Call filter paths first. In the event of none of the
    # paths being valid, get_new_trash_folder wont create a new folder
    paths = read_and_check_paths(files, logger)
    trash_folder = trash.get_new_trash_folder()
    info = Info()

    # Move items to trash folder
    for source in paths:
        dest = move_to_trash(source, trash_folder, logger)
        info.add_move(source.resolve(), dest.resolve())

    info_file = trash_folder / 'dl_info.pickle'
    with open(info_file, 'wb') as f:
        pickle.dump(info, f)
