#!C:\Users\Michael\AppData\Local\Programs\Python\Python37-32\python.exe
"""
pipes.py- a file for redirecting standard files
"""

import sys
import re

from commandparser import CommandParser


class _Pipe:
    pass


class Pipes:
    @classmethod
    def has(cls, other):
        return other in (
            cls.OutToFile,
            cls.OutToIn,
            cls.OutToFileA,
            cls.And,
            cls.AndS,
            cls.Or,
            cls.Cat,
            cls.CatOneLine,
        )

    class OutToIn(_Pipe):
        """
        redirects stdout to stdin
        """
        token = '|'

    class OutToFile(_Pipe):
        """
        redirects stdout to file
        """
        token = '>'

    class OutToFileA(_Pipe):
        """
        appends to file
        """
        token = '>>'

    class And(_Pipe):
        """
        chains 2 commands
        """
        token = '&'

    class AndS(_Pipe):
        """
        does following commands only if previous is successfull
        """
        token = '&&'

    class Or(_Pipe):
        """
        run next command only if previous fails
        """
        token = '||'

    class Cat(_Pipe):
        """
        sends data from file into command
        """
        token = '<'

    class CatOneLine(_Pipe):
        """
        sends one line of the file into command.
        """
        token = '<<'


PIPES = {
    '>': Pipes.OutToFile,
    '>>': Pipes.OutToFileA,
    '<': Pipes.Cat,
    '<<': Pipes.CatOneLine,
    '||': Pipes.Or,
    '|': Pipes.OutToIn,
    '&&': Pipes.AndS,
    '&': Pipes.And,
}


class PipeHandler:
    """
    can handle all of the pipes in a command.
    """

    def __init__(self, cmdstr):
        strings = re.split(r'''(['"].*['"])''', cmdstr)

        is_dstr = re.compile(r'(".*")')
        is_sstr = re.compile(r"('.*')")

        has_pipe = re.compile(r'.*[<>|&]{1,2}.*')

        tokens = []

        for i in strings:
            if is_dstr.match(i):
                tokens.append(i)
                continue

            elif is_sstr.match(i):
                tokens.append(i)
                continue

            elif has_pipe.match(i):
                tokens += (split_pipe(i))
                continue

            tokens.append(i)

        joined = [x.strip() for x in join_on_pipes(tokens)]
        self.tokens = joined

    def create(self):
        """
        returns a list of commmandparser.CommandParser seperated
        by the proper Pipe
        """
        lst = []

        for i, t in enumerate(self.tokens):
            if t in '|| | && & >> > << <'.split():
                lst.append(PIPES[t])

            elif self.tokens[i - 1] in '<'.split():
                lst.append(open(t))

            elif self.tokens[i - 1] in '<<':
                lst.append(open(t, 'r+'))

            elif self.tokens[i - 1] == '>>':
                lst.append(open(t, 'a'))

            elif self.tokens[i - 1] == '>':
                lst.append(open(t, 'w'))

            else:
                lst.append(CommandParser(t))

        return lst

    def run(self):
        """
        finds all commands, joins them linked between
        the proper standard files (stdout, stderr, stdin)
        and chains them properly based on the pipes.
        return exit code of final command
        """
        objs = self.create()

        exitcode = 0
        stdin = None

        for i, obj in enumerate(objs):

            try:
                next = objs[i + 1]
            except IndexError:
                f = isinstance(obj, CommandParser)
                if f:
                    p = obj.get_program()
                    return p(stdin=stdin)[0]
                else:
                    return exitcode
            f = Pipes.has(next)
            if f:
                obj = obj.get_program()

                # next object in list *is* a pipe
                if next == Pipes.OutToIn:
                    exitcode, stdin = obj(stdout=True, stdin=stdin)
                    stdin = stdin.encode()
                    continue

                elif next == Pipes.CatOneLine:
                    stdin = objs[i + 2].readline().encode()
                    exitcode = obj(stdin=stdin)[0]
                    stdin = None
                    break

                elif next == Pipes.Cat:
                    stdin = objs[i + 2].read().encode()
                    exitcode = obj(stdin=stdin)[0]
                    break

                elif next == Pipes.OutToFile or \
                        next == Pipes.OutToFileA:
                    exitcode, stdout = obj(stdout=True, stdin=stdin)
                    stdin = None
                    objs[i + 2].write(stdout.decode())
                    break

                elif next == Pipes.Or:
                    exitcode = obj(stdin=stdin)[0]
                    stdin = None
                    success = not exitcode
                    if success:
                        break

                elif next == Pipes.AndS:
                    exitcode = obj()[0]
                    success = not exitcode
                    stdin = None
                    if not success:
                        break

        return exitcode


def join_on_pipes(tokens):
    """
    joins all tokens, except if they are pipes.
    >>> join_on_pipes(['echo ', "Hello>hi" >> file.txt])
    ['echo "Hello>hi"', '>>',  'file.txt']
    """
    cmds = []
    pipes = []

    at = 0
    while True:
        try:
            token = tokens[at]
        except IndexError:
            break
        if token in '|| | && & >> > << <'.split():
            pipes.append(token)
            at += 1
            continue

        cmd = ''
        try:
            while token not in '|| | && & >> > << <'.split():
                cmd += token
                at += 1
                token = tokens[at]
        except IndexError:
            pass
        cmds.append(cmd)

    # cmds should *always* be 1 index longer than pipes

    pipes.append(None)

    items = []

    for i in zip(cmds, pipes):
        items += i

    items.pop(-1)
    # remove the None

    return items


def split_pipe(string):
    return re.split('([<>|&]{1,2})', string)


print(PipeHandler('cat main.py && echo hi').run())
