"""
this is for reading the script files, and returnning a Script object
that will run the script.
"""

import itertools
import os
import io

if __package__ is not None:
    from pipes.pipehandler import PipeHandler

else:
    import sys
    sys.path.append('..')
    from pipes.pipehandler import PipeHandler


class Script:
    def __init__(self, file):
        self.file = file


    def _iterlines(self):
        for line in self.file:
            yield self.parseline(line)

    def _run_and_set(self, code):
        try:
            exit = code.run()
        except TypeError:
            # command not found
            print(code.tokens[0] + ': command not found!')
            exit = 127

        os.environ['ExitCode'] = repr(exit)


    def parseline(self, line):
        return PipeHandler(line)

    def run(self):
        for i in self._iterlines():
            self._run_and_set(i)

def load(obj):
    if getattr(obj, "read", False):
        return Script(obj)
    raise ArgumentError("Not a file-like object!")

def loads(string):
    return load(open(string))

def _test():
    obj = io.StringIO('echo howdyll\nechode')
    Script(obj).run()

if __name__ == '__main__':
    _test()
