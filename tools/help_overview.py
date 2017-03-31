#!/usr/bin/env python
"""
This is a simple tool to display the help for commands in pywbemcli.

It depends on having a complete list of the commands and subcommands that
are in the tool and simply executes the command and dislays the results

The output normally is in restructuredTxt format but there is an internal flag
to allow pure ascii output.

This was written as a tool to review the pywbemcli commands and options largely
because there is no single overall help that displays the help for all
commands and subcommands.

"""
from __future__ import absolute_import, print_function
import shlex
from subprocess import Popen, PIPE
try:
    import textwrap
    textwrap.indent  # pylint: disable=pointless-statement
except AttributeError:  # undefined function (wasn't added until Python 3.3)
    def indent(text, amount, ch=' '):  # pylint: disable=invalid-name
        """Indent locally define"""
        padding = amount * ch
        return ''.join(padding + line for line in text.splitlines(True))
else:
    def indent(text, amount, ch=' '):  # pylint: disable=invalid-name
        """Wrap textwrap function"""
        return textwrap.indent(text, amount * ch)


ERRORS = 0

# Flag that allows displaying the data as pure text rather than markdown
# format
USE_RST = True


def execute_cmd(cmd_str, shell=False):
    """
    Execute the command in cmd_str and get its exitcode, stdout and stderr.

    This function calls subprocess Popen to be able to execute the
    command and  get stdout, stderr, and the exitcode.

    Parameters:
      cmd_str (:term: `string)
        Command to be executed

      shell (boolean)
        Defines whether shell is to be used to execute the command.  Normally
        the shell should not be required.

    Return:
        Tuple of exitcode, out, err where out and err are strings representing
        the stderr and stdout data
    """
    args = shlex.split(cmd_str)

    proc = Popen(args, stdout=PIPE, stderr=PIPE, shell=shell)
    std_out_str, std_err_str = proc.communicate()
    exitcode = proc.returncode

    # return tuple of exitcode, stdout, stderr
    return exitcode, std_out_str, std_err_str


def rst_headline(title, level):
    """
    Format a markdown header line based on the level argument. The rst format
    for headings is generally of the form
    ====================
    title for this thing
    ====================
    """
    level_char_list = ['#', '*', '=', '-', '^', '"']
    try:
        level_char = level_char_list[level]
    except IndexError:
        level_char = '='

    return '\n%s\n%s\n%s\n' % (level_char * len(title),
                               title,
                               (level_char * len(title)))


def print_rst_verbatum_text(text_str):
    """
    Print the text on input surrounded by the back quotes defining
    veratum text
    """
    print('::\n')
    # indent text for rst. rst requires that block monospace test be
    # indented and preceeded by line with just '::' and followed by
    # empty line. This indents by two char the complete test_str except
    # the first line
    print('%s\n' % indent(text_str, 4))


def help_cmd(cmd_str):
    """Output a command created from the input and test result.
    """
    global ERRORS  # pylint: disable=global-statement

    if isinstance(cmd_str, list):
        for cmd in cmd_str:
            help_cmd(cmd)
    else:
        command = 'pywbemcli %s --help' % (cmd_str)
        if USE_RST:
            print(rst_headline(command, 1))
        else:
            print('%s\nPYWBEMCLI COMMAND: %s' % (('=' * 50), command))

        exitcode, out, err = execute_cmd(command)

        if USE_RST:
            print_rst_verbatum_text(out)
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
print(rst_headline(
    'Overview of pywbemcli help with the multiple subcommands', 0))

print('This is a display of the output of the pywbemcli commands define in '
    'this file. Each help output is presented as a section title with the '
    'command as sent to pywbemcli followed by the ouput returned by '
    'pywbemcli.'     )

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

help_cmd("connection show")

if ERRORS != 0:
    print('%s ERRORS encountered in output' % ERRORS)
