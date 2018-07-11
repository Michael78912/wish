"""
pipes.py- a file for redirecting standard files
"""

class _Pipe:
    pass

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
