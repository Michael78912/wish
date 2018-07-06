"""
commands.py- database of all commands.
_Command is a base class for any command
"""

__version__ = '0.0a'
__author__ = 'Michael Gill <michaelveenstra12@gmail.com>'
__all__ = ['ls', 'pwd']

import os
import shutil
import re
import argparse

from lsutils import _LsItem


class _Command:
    def __init__(self, func):
        self.func = func
        self.__doc__ = func.__doc__

    def __call__(self, args):
        return self.parser(self, args)

    def argparse(self, parser):
        self.parser = parser


@_Command
def pwd():
    print(os.getcwd())
    return 0


@pwd.argparse
def pwd_parse(cmd, args):
    parser = argparse.ArgumentParser(description='output current directory')
    parser.add_argument(
        '-v',
        '--version',
        action='store_true',
        help='display version information and exit.')

    ns = parser.parse_args(args)

    if ns.version:
        print("pwd (WISH version) 0.0a")
        return 0

    return cmd.func()


@_Command
def ls(self, directory='.', colour=True, show_hidden=False):
    """
    list directory contents of directory.
    mode can be columned, rowed, or normal (horizontal and vertical,
    1 space padding.
    """
    raw = os.listdir(directory)
    string = ''
    # print(raw)
    colourer = _get_coloured_str if colour else lambda x: x

    try:
        for item in raw:
            _LsItem(os.path.join(directory, item))

    except (PermissionError, OSError):
        print('ls: %s: Permission Denied' % directory)
        return 1

    print(_LsItem.sort(show_hidden))
    _LsItem.clear()
    return 0


@ls.argparse
def ls_parser(cmd, args):
    parser = argparse.ArgumentParser(description="list directory contents")
    parser.add_argument(
        'dir',
        default='.',
        nargs='?',
        help='Directory to evaluate. defaults to .')
    parser.add_argument(
        '-a',
        '--all',
        action='store_true',
        help='list dot (.) suffixed names as well')
    parser.add_argument(
        '-c',
        '--colour',
        action='store_true',
        help=
        'display contents with colour. type "ls --list-colour to see these."')
    parser.add_argument(
        '--list-colour',
        action='store_true',
        help='see list of colours and their meanings.')
    parser.add_argument(
        '-v',
        '--version',
        action='store_true',
        help='display version information and exit.')

    ns = parser.parse_args(args)

    if ns.version:
        print('ls (WISH version) 0.0a')
        return 0

    if ns.list_colour:
        print("""ls colours and their meanings:
            black on red: a broken symlink
            cyan on black: symlink
            blue on black: Directory
            red on black: archive file
            magenta on black: windows shortcut (*.lnk)
            green on black: executable file (extension in PATHEXT)
            white on black: other file""")

        return 0

    kwargs = {
        'directory': ns.dir,
        'colour': ns.colour,
        'show_hidden': ns.all,
    }

    return cmd.func(cmd, **kwargs)


if __name__ == '__main__':
    ls(['--help'])
