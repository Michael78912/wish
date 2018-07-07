"""
commands.py- database of all commands.
_Command is a base class for any command
"""

__version__ = '0.0a'
__author__ = 'Michael Gill <michaelveenstra12@gmail.com>'
__all__ = ['ls', 'pwd', 'cd', 'mkdir', 'echo', 'cat', 'alias']

import os
import shutil
import re
import argparse

from lsutils import _LsItem
from aliasutils import CommandParser

VHELP = 'display version information and exit.'
ALIAS = {}


class _Command:
    def __init__(self, func):
        self.func = func
        self.__doc__ = func.__doc__

    def __call__(self, args):
        try:
            return self.parser(self, args)
        except SystemExit:
            # arparse thinks it needs to exit, command missing
            return 1

    def argparse(self, parser):
        self.parser = parser

@_Command
def alias(cmd, alias):
    """
    tell the command interpreter that alias is equal to cmd
    """
    command = CommandParser(cmd)
    try:
        ALIAS[alias] = command.get_program()
    except TypeError:
        print(command.args[0] + 'command not found')
        return 1
    return 0

@alias.argparse
def alias_parse(cmd, args):
    parser = argparse.ArgumentParser(description='create an alias for a command', prog='alias')
    parser.add_argument('alias', help='new name to assign command')
    parser.add_argument('command', help='command to create the alias for. must be quoted to include multiple arguments.')
    parser.add_argument('-v', '--version', action='store_true', help=VHELP)

    ns = parser.parse_args(args)

    if ns.version:
        print('alias (WISH Version) 0.0a')
        return 0

    return cmd.func(ns.command, ns.alias)



@_Command
def cat(fname, newline=True):
    """
    output the file contents to stdout
    """
    try:
        print(open(fname).read())
        return 0

    except PermissionError:
        print(fname + ': Permission Denied')
        return 1

    except FileNotFoundError:
        print(fname + ': File Not Found!')
        return 1


@cat.argparse
def cat_parse(cmd, args):
    parser = argparse.ArgumentParser(
        description="display contents of the file given")
    parser.add_argument('file', help="display the contents of this file")
    parser.add_argument(
        '-n',
        '--no-newline',
        action='store_true',
        dest='newline',
        help='dont add a newline to the end')
    parser.add_argument('-v', '--version', action='store_true', help=VHELP)

    ns = parser.parse_args(args)

    if ns.version:
        print('cat (WISH Version) 0.0a')
    return cmd.func(ns.file, ns.newline)



@_Command
def echo(string, newline=True, interpret=False):
    """
    write output given to this command.
    backslash escapes: these can be given, and will be evaluated.
    if you want to include a backslash escapped character, escape it with
    another backslash. (only applies in backslash interpretation mode (-e))"""
    if interpret:
        string = bytes(string, 'utf-8').decode('unicode_escape')

    print(string, end='\n' if newline else '')
    return 0


@echo.argparse
def echo_parse(cmd, args):
    parser = argparse.ArgumentParser(
        description='output the given argument', prog='echo')
    parser.add_argument(
        'arg', nargs='*', help='display the given output.', default=[])
    parser.add_argument(
        '-n',
        '--no-newline',
        action='store_false',
        help='use this if you dont want a newline at the end of the output')
    parser.add_argument(
        '-e',
        '--interpret',
        action='store_true',
        help='interpret backslashes as escape codes.')
    parser.add_argument('-v', '--version', action='store_true', help=VHELP)

    ns = parser.parse_args(args)

    if ns.version:
        print('echo (WISH version) 0.0a')
        return 0

    echo_opts = {
        'string': ' '.join(ns.arg),
        'newline': ns.no_newline,
        'interpret': ns.interpret,
    }

    return cmd.func(**echo_opts)


@_Command
def mkdir(directory):
    """
    create a Directory
    """
    try:
        os.mkdir(directory)

    except FileNotFoundError:
        print('File not found')
        return 1

    except PermissionError:
        print(directory + ': Access Denied')
        return 1
    return 0


@mkdir.argparse
def mkdir_parse(cmd, args):
    parser = argparse.ArgumentParser(
        description='create a directory', prog='mkdir')
    parser.add_argument('name', help='create directory <name>')
    parser.add_argument('-v', '--version', action='store_true', help=VHELP)

    ns = parser.parse_args(args)

    if ns.version:
        print('mkdir (WISH VERSION) 0.0a')
        return 0

    return cmd.func(ns.name)


@_Command
def cd(directory):
    """
    change the current Directory
    """
    os.chdir('.')
    return 0


@cd.argparse
def cd_parse(cmd, args):
    parser = argparse.ArgumentParser(
        description="change current directory", prog='cd')
    parser.add_argument('-v', '--version', action='store_true', help=VHELP)
    parser.add_argument('directory', help='where to change to')

    ns = parser.parse_args(args)

    if ns.version:
        print("cd (WISH version) 0.0a")
        return 0

    return cmd.func(directory=ns.directory)


@_Command
def pwd():
    """
    Print Working Directory (an abbreviation! (It took me years to see that))
    """
    print(os.getcwd())
    return 0


@pwd.argparse
def pwd_parse(cmd, args):
    parser = argparse.ArgumentParser(
        description='output current directory', prog='pwd')
    parser.add_argument('-v', '--version', action='store_true', help=VHELP)

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
    parser = argparse.ArgumentParser(
        description="list directory contents", prog='ls')
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
    parser.add_argument('-v', '--version', action='store_true', help=VHELP)

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
