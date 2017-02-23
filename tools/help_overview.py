#!/usr/bin/env python
"""
This is a simple tool to display the help for commands in pywbemcli.

It depends on having a complete list of the commands and subcommands that
are in the tool and simply executes the command and dislays the results

The output normally is in markdown format but there is an internal flag
to allow pure ascii output.

This was written as a tool to review the pywbemcli commands and options largely
because there is no single overall help that displays the help for all
commands and subcommands.

"""
from __future__ import absolute_import, print_function
import shlex
from subprocess import Popen, PIPE
import os


ERRORS = 0

# Flag that allows displaying the data as pure text rather than markdown
# format
USE_MD = True

def get_exitcode_stdout_stderr(cmd):
    """
    Execute the external command and get its exitcode, stdout and stderr.
    """
    args = shlex.split(cmd)

    proc = Popen(args, stdout=PIPE, stderr=PIPE)
    out, err = proc.communicate()
    exitcode = proc.returncode
    #
    return exitcode, out, err

def md_headline(title, level):
    """
    Format a markdown header line based on the level argument
    """
    level_char_list = ['=', '-']
    try:
        level_char = level_char_list[level]
    except IndexError:
        level_char = '='

    return '\n%s\n%s\n' % (title, (level_char * len(title)))

def print_md_verbatum_text(text_str):
    """
    Print the text on input surrounded by the back quotes defining
    veratum text
    """
    print('```')
    print(text_str)
    print('```')    

def help_cmd(cmd_str):
    """Output a command created from the input and test result.
    """
    global ERRORS
    global USE_MD

    if isinstance(cmd_str, list):
        for cmd in cmd_str:
            help_cmd(cmd)
    else:    
        command = 'pywbemcli %s --help' % (cmd_str)
        if USE_MD:
            print(md_headline(command, 0))
        else:
            print('%s\nPYWBEMCLI COMMAND: %s' % (('=' * 50),command))
      
        exitcode, out, err = get_exitcode_stdout_stderr(command)
        
        if USE_MD:
            print_md_verbatum_text(out)
        else:            
            print(out)
        if err:
            print('**STDER:** %s' % err)

        if exitcode != 0:
            ERRORS += 1
            print('**ERROR:** cmd `%s`' % command)

#
#  List of the help commands
#
print('**Overview of pywbemcli help with the multiple subcommands***\n\n')

help_cmd("")
help_cmd("class")
help_cmd("class get")
help_cmd("class invokemethod")
help_cmd("class names")
help_cmd("class enumerate")
help_cmd("class associators")
help_cmd("class references")
help_cmd("class find")
help_cmd("class hierarchy")

help_cmd("instance get")
help_cmd("instance delete")
help_cmd("instance create")
help_cmd("instance invokemethod")
help_cmd("instance query")
help_cmd("instance names")
help_cmd("instance enumerate")
help_cmd("instance count")
help_cmd("instance references")
help_cmd("instance associators")

help_cmd("qualifier")
help_cmd("qualifier enumerate")
help_cmd("qualifier get")

help_cmd("server")
help_cmd("server brand")
help_cmd("server connection")
help_cmd("server info")
help_cmd("server namespaces")
help_cmd("server interop")
help_cmd("server profiles")

if ERRORS != 0:
    print('%s ERRORS encountered in output' % ERRORS)
