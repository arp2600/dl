#!/usr/bin/env python3
import trash
import subprocess


def run(logger):
    trash_path = trash.get_trash_path()

    logger.print('Emptying {}'.format(trash_path), 1)
    logger.print('', 2)

    if trash_path:
        cmd = ['rm', '-rfv', trash_path]
        print('{}'.format(' '.join(map(str, cmd))))
        subprocess.run(cmd)
