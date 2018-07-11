"""
pipes.py- a file for redirecting standard files
"""

import re


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


class PipeHandler:
    """
    can handle all of the pipes in a command.
    """
    def __init__(self, cmdstr):
        print(re.findall(r'''(?[\|&<>][^'"])[\|&<>]([\|&<>]:[^'"])''', cmdstr))
        pipes = [x.strip() for x in re.findall(r'''[^'"][\|&><]{1}[^'"]|([<>\|&]|(<<|>>|&&|\|\|))''', cmdstr)]
        cmds = [x.strip() for x in re.split(r'''[^'"][\|&><]{1}[^'"]''', cmdstr)]
        print(pipes, cmds)

        tokens = []
        for i, p in enumerate(pipes):
            tokens += [cmds[i], p]
        tokens.append(cmds[i + 1])
        print(tokens)


PipeHandler('echo "howdy>hi" |tee tuna.txt > tuna.txt')
