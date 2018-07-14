"""
pipes.py- a file for redirecting standard files
"""

from io import TextIOWrapper
import re


from commandparser import CommandParser


class _Pipe:
    pass


class Pipes:
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

            elif self.tokens[i -1] == '>':
                lst.append(open(t, 'w'))

            else:
                lst.append(CommandParser(t))

        return lst

    def apply(self):


    # def run(self):
    #     objects = self.create()
    #     for i, obj in enumerate(objects):
    #         if issubclass(_Pipe, obj.__class__):
    #             # pipes are only needed to
    #             continue
    #         try:
    #             pipe = objects.index(obj)



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


# print(split_pipe('Hi > hioh >> jij'))
print(PipeHandler('tee hi << main.py').create())
# print(join_on_pipes(['howdy', '>>', 'boi', '"no"', 'kill me now']))
