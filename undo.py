import sys
import pickle
import trash
from print_functions import print_error, print_move


def run(args):
    trash_folders = trash.get_trash_folders()
    if len(trash_folders) == 0:
        print_error('Trash is empty')
        sys.exit(1)

    undo_folder = trash_folders[-1]
    info_file = undo_folder / 'dl_info.pickle'
    with open(info_file, 'rb') as f:
        info = pickle.load(f)

    for source, dest in info.moves:
        print_move(source, dest, args.verbose)
        if not source.parent.exists():
            source.parent.mkdir(parents=True)

        dest.rename(source)

    info_file.unlink()
    undo_folder.rmdir()
