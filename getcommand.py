from commandparser import CommandParser

def getcommand(cmdstr):
    """
    returns a callable object that runs as a command, and returns
    an exit code.
    """

    x = CommandParser(cmdstr)
    try:
        return x.get_program()
    except TypeError:
        print(x.args[0] + ': command not found!')
        return lambda: 127

def runcommand(cmdstr):
    """
    run command, and return exit code.
    """
    return getcommand(cmdstr)()
