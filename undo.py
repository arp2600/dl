import sys
import pickle
from trash import *


def run(args):
    trash_folders = get_trash_folders()
    if len(trash_folders) == 0:
        print('Trash is empty')
        sys.exit(1)

    undo_folder = trash_folders[-1]
    info_file = undo_folder / 'dl_info.pickle'
    with open(info_file, 'rb') as f:
        info = pickle.load(f)

    for source, dest in info.moves:
        print('Restoring {}'.format(source))
        if not source.parent.exists():
            source.parent.mkdir(parents=True)

        dest.rename(source)

    info_file.unlink()
    undo_folder.rmdir()
