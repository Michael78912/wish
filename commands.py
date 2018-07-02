"""
commands.py- database of all commands.
_Command is a base class for any command
"""

__version__ = '0.0a'
__author__ = 'Michael Gill <michaelveenstra12@gmail.com>'

import os
import shutil
import re

import colorama as cm

_LS_COLOURS = {
    'broken-symlink': (cm.Fore.BLACK, cm.Back.RED),
    'symlink':        (cm.Fore.CYAN, cm.Back.BLACK),
    'directory':      (cm.Fore.BLUE, cm.Back.BLACK),
    'archive':        (cm.Fore.RED, cm.Back.BLACK),
    'other':          (cm.Fore.WHITE, cm.Back.BLACK),
    'shortcut':       (cm.Fore.MAGENTA, cm.Back.BLACK),
    'executable':     (cm.Fore.GREEN, cm.Back.BLACK),
}

_EXECUTABLE_EXTENSIONS = os.environ.get('PATHEXT')\
                         .lower().strip('.').split(';.')\
                         or ['exe', 'com', 'bat', 'cmd']

_ARCHIVE_EXTENSIONS = [
    'tar', 'zip', 'gz', 'tgz', '7z', 'rar', 'xz', 'lzma',
    'iso', 'bz2', 'bz', 'dmg', 'cab', 'jar', 'pyz'
]

# print(_ARCHIVE_EXTENSIONS, _EXECUTABLE_EXTENSIONS)

class _Command:
    def __init__(self, func):
        self.func = func
        self.__doc__ = func.__doc__

    def __call__(self, *args, **kwargs):
        self.func(*args, **kwargs)


def _get_coloured_str(filename):
    """
    returns the proper string, padded by proper
    colours on the file type.
    """

    if os.path.islink(filename):
        try:
            os.stat(filename)
            colour = _LS_COLOURS['symlink']
        except OSError:
            # the link is broken
            colour = _LS_COLOURS['broken symlink']

    elif os.path.isdir(filename):
        colour = _LS_COLOURS['directory']

    else:
        # we are now relying on the extension
        try:
            extension = filename.split('.')[-1]
        except IndexError:
            # file has no extension
            extension = None
            colour = _LS_COLOURS['other']

        if extension is not None:
            if extension in _ARCHIVE_EXTENSIONS:
                colour = _LS_COLOURS['archive']

            elif extension in _EXECUTABLE_EXTENSIONS:
                colour = _LS_COLOURS['executable']

            elif extension == 'lnk':
                colour = _LS_COLOURS['shortcut']

            else:
                colour = _LS_COLOURS['other']

    return ''.join(colour + (filename.split('\\')[-1], cm.Style.RESET_ALL))



@_Command
def ls(self, directory='.', mode='normal', colour=True):
    """
    list directory contents of directory.
    mode can be columned, rowed, or normal (horizontal and vertical,
    1 space padding.
    """
    raw = os.listdir(directory)
    string = ''
    sz = shutil.get_terminal_size()[0]
    if mode == 'normal':
        at = 0
        while True:
            str1 = raw[at]
            f1 = os.path.join(directory, str1)
            str2 = raw[at + 1]
            if ' ' in str1:
                str1 = "'" + str1 + "'"
            if ' ' in str2:
                str2 = "'" + str2 + "'"
            str1 = str1.ljust(sz // 2, ' ')
            str2 = str2.rjust(sz // 2, ' ')
            string += str1 + str2 + '\n'
            at += 2

    print(string)

print(ls(ls))
