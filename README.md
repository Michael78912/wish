# <img src="https://raw.githubusercontent.com/Michael78912/wish/master/img/ico.png" alt="icon" width=64 height=64></img> WISH 
### Windows Improved SHell

![LS command](https://raw.githubusercontent.com/Michael78912/wish/master/img/ls.PNG)

this aims at being an improved shell for windows.  
I started making this because I was fed up with cmd.exe  
I haven't thought of anything else to put here yet, so there you go.  

## UPDATE:  July 6, 2018
I've worked this into a somewhat usable state. it now supports calling external programs, a _few_ internal commands (many more being developed), and readline-style tab complete.  
built in commands so far include:

`ls`, `cd`, `mkdir`, `pwd`, `cat`, `alias`, `echo`, `help`, `set`. yeah, I know thats barely anything, I'm still working on it :P  

## Need to do:
- make many more commands (grep, read, etc...)
- allow all extensions in %PATHEXT% to be called as programs (access default programs through registry)
- enable piping :check:
- enable access to environment variables
- **scripting** (thats a big one)
- different prompts (I want there to be a bunch of different kinds of prompts)
- initiation script

## Piping:
as of July 15, piping now works! it has 8.
- `command > file`: sends stdout from command to file (overwrites previous content, creates if non-exisistant)
- `command >> file`: sends stdout from command to fil (appends, creates if non-existent)
- `command1 | command2`: sends stdout from command1 to stdin of command2
- `command1 || command2`: does command2 *only* if command1 fails (exits on non-zero return code)
- `command1 & command2`: does command1, and then command2
- `command1 && command2`: does command1, then command2 if command1 succeeds (exits on zero return code)
- `command < file`: reads file, and sends contents to stdin of command (equivalent to `cat file | command`)
- `command << file`: reads **one line** of file and sends that to stdin of command  
  
#### *if you have any more ideas, please comment about them! any suggestions will be looked at!*
