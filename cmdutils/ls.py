"""
lsutils.py- i did this to have commands.py more readable.
"""

import os

import colorama as cm

cm.init()

_LS_COLOURS = {
    'broken-symlink': (cm.Fore.BLACK, cm.Back.RED),
    'symlink':        (cm.Fore.CYAN, cm.Back.BLACK),
    'directory':      (cm.Fore.BLUE, cm.Back.BLACK),
    'archive':        (cm.Fore.RED, cm.Back.BLACK),
    'other':          (cm.Fore.WHITE, cm.Back.BLACK),
    'shortcut':       (cm.Fore.MAGENTA, cm.Back.BLACK),
    'executable':     (cm.Fore.GREEN, cm.Back.BLACK),
}

PRIORITIES = ['broken-symlink', 'directory', 'symlink', 'shortcut',
'executable', 'other']

_EXECUTABLE_EXTENSIONS = os.environ.get('PATHEXT')\
                         .lower().strip('.').split(';.')\
                         or ['exe', 'com', 'bat', 'cmd']

_ARCHIVE_EXTENSIONS = [
    'tar', 'zip', 'gz', 'tgz', '7z', 'rar', 'xz', 'lzma',
    'iso', 'bz2', 'bz', 'dmg', 'cab', 'jar', 'pyz'
]

def _get_coloured_str(filename):
    """
    returns the proper string, padded by proper
    type_s on the file type.
    """

    if os.path.islink(filename):
        try:
            os.stat(filename)
            colour = _LS_COLOURS['symlink']
        except OSError:
            # the link is broken
            colour = _LS_COLOURS['broken-symlink']

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

class LsItem:
    """
    base class for ls files.
    """
    instances = []
    def __init__(self, path, set_colour=True):
        self.__class__.instances.append(self)
        self.path = path
        self.fname = path.split('\\')[-1]
        self.coloured_fname = _get_coloured_str(path)
        self.set_colour = set_colour

    def __repr__(self):
        return self.coloured_fname if self.set_colour else self.fname

    def __del__(self):
        self.__class__.instances = []

    @classmethod
    def add_all(cls, joiner='\n'):
        """
        add every item in cls.instances, and return them joined
        by joiner.
        """
        return joiner.join(map(lambda x: repr(x), cls.instances))

    @classmethod
    def clear(cls):
        """
        clear all instances from cls.
        """
        cls.instances = []

    @classmethod
    def sort(cls, showdot=True):
        priority = {}
        for key in _LS_COLOURS.keys():
            priority[key] = []

        for item in cls.instances:
            filename = item.path
            if os.path.islink(filename):
                try:
                    os.stat(filename)
                    type_ = 'symlink'
                except OSError:
                    # the link is broken
                    type_ = 'broken-symlink'

            elif os.path.isdir(filename):
                type_ = 'directory'

            else:
                # we are now relying on the extension
                try:
                    extension = filename.split('.')[-1]
                except IndexError:
                    # file has no extension
                    extension = None
                    type_ = 'other'

                if extension is not None:
                    if extension in _ARCHIVE_EXTENSIONS:
                        type_ = 'archive'

                    elif extension in _EXECUTABLE_EXTENSIONS:
                        type_ = 'executable'

                    elif extension == 'lnk':
                        type_ = 'shortcut'

                    else:
                        type_ = 'other'
            priority[type_].append(item)

        string = ''
        for type_ in PRIORITIES:
            for item in priority[type_]:
                if item.fname.startswith('.') and not showdot:
                    continue
                string += repr(item) + '\n'

        return string
