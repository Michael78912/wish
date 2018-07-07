import re
import os

import commands

PATHEXT = os.environ['pathext'].split(';')
PATH = os.environ['path'].split(';') + [os.getcwd()]

def _get_path():
    d = []
    for path in PATH:
        if os.path.isdir(path):
            d += os.listdir(path)
        else:
            d += [path]
    # print(len(d))
    # print(tuple(os.getenv('pathext').split(';')))
    return d

PATH_CMDS = list(
    filter(
        lambda x: x.upper().endswith(tuple(os.getenv('pathext').split(';'))),
        _get_path()))
ALL_CMDS = commands.__all__ + PATH_CMDS
PATH_CMDS = [i.upper() for i in PATH_CMDS]

def _get_path():
    d = []
    for path in PATH:
        if os.path.isdir(path):
            d += os.listdir(path)
        else:
            d += [path]
    # print(len(d))
    # print(tuple(os.getenv('pathext').split(';')))
    return d
class _PathCmds:
    base = PATH_CMDS

    def __contains__(self, item):
        item = item.upper()
        for i in PATHEXT:
            if item + i in self.base or item in self.base:
                return True
        return False

    def __iter__(self):
        for i in self.base:
            yield i

    def __getitem__(self, item):
        item = item.upper()
        for i in PATHEXT:
            if item + i in self.base:
                print(item + i)
                return item + i

            elif item in self.base:
                print(item)
                return item


PATH_CMDS = _PathCmds()


class CommandParser:
    def __init__(self, cmdstr):
        self.cmdstr = cmdstr
        self.args = self.rm_strings()

    def rm_strings(self):
        stringsplit = re.split('(".*")', self.cmdstr)
        lst = []
        for i in stringsplit:
            lst += i.split() if not re.match('".*"', i) else [i.strip('""')]

        return lst

    def get_program(self):
        # print(self.args[0])
        cmd = None

        if self.args[0] in commands.__all__:
            # built-in command
            # print('found command in commands.__all__')
            cmd_f = getattr(commands, self.args[0])

            def cmd(): return cmd_f(self.args[1:])

        elif self.args[0] in PATH_CMDS:
            cmd = _ExecutableCommand(PATH_CMDS[self.args[0]], self.args[1:])

        if cmd == None:
            raise TypeError('Command ')
        return cmd
