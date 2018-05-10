import re
import humanfriendly as hf
from pathlib import Path

_home = Path.home()


def get_trash_path():
    trash_path = _home / '.dl' / 'trash'
    if not trash_path.exists():
        trash_path.mkdir(parents=True)

    return trash_path


def get_trash_folders(trash_path=None):
    if not trash_path:
        trash_path = get_trash_path()

    # User the contents of trash to work out
    # the number for the next trash folder
    pattern = re.compile('^\d+$')
    condition = lambda x: x.is_dir and pattern.match(x.name)
    trash_contents = [x for x in trash_path.iterdir() if condition(x)]
    trash_contents.sort(key=lambda x: int(x.name))

    return trash_contents


def get_new_trash_folder(trash_path=None):
    if not trash_path:
        trash_path = get_trash_path()
    trash_contents = get_trash_folders(trash_path)

    if trash_contents:
        next_trash_folder = max([int(i.name) for i in trash_contents]) + 1
        next_trash_folder = next_trash_folder
    else:
        next_trash_folder = 0

    next_trash_folder = '{:04d}'.format(next_trash_folder)

    trash_folder = trash_path / next_trash_folder
    trash_folder.mkdir()

    return trash_folder


def print_size(verbosity=0):
    path = get_trash_path()
    paths = [path for path in path.glob('**/*') if path.is_file()]
    if verbosity > 0:
        paths.sort(key=lambda x: x.stat().st_size)
        for path in paths:
            file_size = path.stat().st_size
            readable_size = hf.format_size(file_size)
            print('{}  {}'.format(readable_size, path))
        print('')

    size_in_bytes = sum([p.stat().st_size for p in paths])

    readable_size = hf.format_size(size_in_bytes)
    print('Trash size is {}'.format(readable_size))
