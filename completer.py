import readline
import os
import commands

ALL_CMDS = commands.__all__
for path in os.environ['Path'].split(';'

class SimpleCompleter:
    """
    a simple class for tab completion.
    "borrowed" from https://pymotw.com/2/readline/
    converted to python3 syntax, however
    """
    def __init__(self, options):
        self.options = sorted(options)
        return

    def complete(self, text, state):
        response = None
        if state == 0:
            # This is the first time for this text, so build a match list.
            if text:
                self.matches = [s 
                                for s in self.options
                                if s and s.startswith(text)]
            else:
                self.matches = self.options[:]
        
        # Return the state'th item from the match list,
        # if we have that many.
        try:
            response = self.matches[state]
        except IndexError:
            response = None
        return response


def init():
    readline.set_completer(SimpleCompleter().complete)
    
    readline.parse_and_bind('tab: complete')
