import sys
import pickle
import trash


def run(logger):
    trash_folders = trash.get_trash_folders()
    if len(trash_folders) == 0:
        logger.error('Trash is empty')
        sys.exit(1)

    undo_folder = trash_folders[-1]
    info_file = undo_folder / 'dl_info.pickle'
    with open(info_file, 'rb') as f:
        info = pickle.load(f)

    for source, dest in info.moves:
        logger.print_move(dest, source)
        if not source.parent.exists():
            source.parent.mkdir(parents=True)

        dest.rename(source)

    info_file.unlink()
    # when items are deleted with an absolute path
    # an extra directory gets made in the trash folder
    for item in undo_folder.iterdir():
        logger.print("removing {}".format(item), 0)
        item.rmdir()
    undo_folder.rmdir()
