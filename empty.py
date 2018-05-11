#!/usr/bin/env python3
import trash


class Deleter:
    def __init__(self, logger):
        self.logger = logger
        self.file_count = 0
        self.directory_count = 0

    def delete_path(self, path):
        for item in path.glob('*'):
            self.delete_path(item)

        if path.is_dir():
            self.logger.print('rmdir {}'.format(path), 2)
            path.rmdir()
            self.directory_count += 1
        else:
            self.logger.print('rm {}'.format(path), 2)
            path.unlink()
            self.file_count += 1


def run(logger):
    trash_path = trash.get_trash_path()

    logger.print('Emptying {}'.format(trash_path), 1)
    logger.print('', 2)

    deleter = Deleter(logger)
    deleter.delete_path(trash_path)

    logger.print('', 2)
    logger.print('Removed {} items'.format(
        deleter.file_count + deleter.directory_count), 1)
    logger.print('  {} files'.format(deleter.file_count), 1)
    logger.print('  {} directories'.format(deleter.directory_count), 1)
