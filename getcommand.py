import os


from pipes import PipeHandler

def getcommand(cmdstr):
    """
    returns a callable object that runs as a command, and returns
    an exit code.
    """

    x = PipeHandler(cmdstr)
    try:
        return x.run()
    except TypeError:
        print(x.tokens[0] + ': command not found!')
        return 127


def runcommand(cmdstr, set_var=True):
    """
    run command, and return exit code.
    """
    code = getcommand(cmdstr)
    if set_var:
        os.environ['ExitCode'] = repr(code)

    return code
