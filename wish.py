#!C:\Users\Michael\AppData\Local\Programs\Python\Python37-32\python.exe

"""
WISH: Windows Improved SHell
this shell aims at being much more efficient than cmd.exe,
more useful, and easier scripting.
"""

__author__ = 'Michael Gill <michaelveenstra12@gmail.com>'
__version__ = '0.0a'

import argparse
import sys
import os
import colorama
import ctypes
import re

from scripting.parser import loads
import completer
import getcommand

def main():
    """
    gather arguments and start shell.
    """

    # initiate the colorama module for windows
    colorama.init()
    completer.init()
    ctypes.windll.kernel32.SetConsoleTitleW('WISH@' + os.getcwd())

    # create argument parser
    parser = argparse.ArgumentParser(
        description="an improved shell for Windows")

    # add optional arguments
    parser.add_argument(
        '--script', '-s', help='script file to be run', dest='file', type=loads)
    parser.add_argument(
        '-c', help='execute string and exit', dest='code', type=str)
    parser.add_argument(
        '--version',
        '-v',
        help='display version information and exit',
        action='store_true')

    # generate sorted arguments
    try:
        namespace = parser.parse_args()

    except FileNotFoundError:
        print('file not found!')
        raise SystemExit(2)

    # -v or --version were passed
    if namespace.version:
        print(version)
        raise SystemExit

    # -s or --script were passed
    if namespace.file:
        namespace.file.run()
        raise SystemExit

    while True:
        print(
            colorama.Fore.RED + os.getlogin() + ': ' + colorama.Fore.BLUE +
            os.getcwd() + colorama.Fore.GREEN + '$ ' + colorama.Fore.RESET,
            end='')

        try:
            command = input()
            if command == '':
                continue

            if re.match('exit\s+.*', command, re.IGNORECASE):
                code = re.match('exit\s+(.*)').group(1)
                try:
                    code = int(code)
                except ValueError:
                    code = 0
                raise SystemExit(code)
            elif command.lower().strip() == 'exit':
                raise SystemExit(0)

            getcommand.runcommand(command)
            completer.init()
            ctypes.windll.kernel32.SetConsoleTitleW('WISH@' + os.getcwd())

        except (EOFError, KeyboardInterrupt):  # Ctrl + C or Ctrl + Z + Enter
            raise SystemExit(0)

if __name__ == '__main__':
    main()
