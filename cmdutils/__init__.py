"""
this package is for files, used by commands in commands.py.
my rule is that each command has *only* 2 functions in it,
the main one and the parser. if it has anything else, it should go
here in a file called <command name>.py. you can then call
from cmdutils.cmd import thing1, thing2, thing3.
then you can use them like that.
I realized this problem a bit before, so i put them in 2 files,
aliasutils.py and lsutils.py. they cluttered up the directory, so i'll move
them here.
"""

__author__ = 'Michael Gill <michaelveenstra12@gmail.com>'
