#!/usr/bin/env python

"""
This tool can capture the help outputs from a click application and output
the result either as text or in restructured text format.

It executes the click script --help and recursively scrapes all of the
commands from the output, generating an output that is the help text for
every group/command in the script.

All output is to stdout.

It will generate either restructured text (RST) or pure text output depending on
the variable USE_RST.

The RST output sets a section name for each help subject.

This tool is useable with different click generated apps by passing the script
name as a command line parameter.
"""

from __future__ import print_function, absolute_import

import sys
import subprocess
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

import six

# Flag that controls the output format. If True, generates .rst output.
# Otherwise it generates pure formatted text.
USE_RST = True

if len(sys.argv) != 2:
    print("Usage: {} SCRIPT_NAME".format(sys.argv[0]))
    sys.exit(2)

SCRIPT_NAME = sys.argv[1]
SCRIPT_CMD = SCRIPT_NAME

ERRORS = 0
VERBOSE = False


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

    # output anchor in form .. _`smicli commands`:
    anchor = '.. _`{}`:'.format(title)
    title_marker = level_char * len(title)
    if level == 0:
        return '\n{}\n\n{}\n{}\n{}\n'.format(anchor, title_marker, title,
                                             title_marker)

    return '\n{}\n\n{}\n{}\n'.format(anchor, title, title_marker)


def print_rst_verbatum_text(text_str):
    """
    Print the text on input proceeded by the rst literal block indicator
    """
    print('::\n')
    # indent text for rst. rst requires that block monospace test be
    # indented and preceeded by line with just '::' and followed by
    # empty line. Indent all lines with text

    lines = text_str.split('\n')
    new_lines = []
    for line in lines:
        if line:
            new_lines.append(indent(line, 4))
        else:
            new_lines.append(line)
    print('{}'.format('\n'.join(new_lines)))


HELP_DICT = {}


def cmd_exists(cmd):
    """
    Determine if the command defined by cmd can be executed in a shell.

    Returns a tuple (rc, msg), where rc==0 indicates that the command can be
    executed, and otherwise rc is the command (or shell) return code and
    msg is an error message.
    """

    proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE,
                            stderr=subprocess.STDOUT)
    out, _ = proc.communicate()
    rc = proc.returncode
    if rc == 0:
        msg = None
    else:
        msg = out.strip()
    return rc, msg


def get_subcmd_group_names(script_cmd, script_name, cmd):
    """
    Execute the script with defined command and help and get the
    groups defined for that help.

    returns list of command groups/commands
    """
    command = '{} {} --help'.format(script_cmd, cmd)
    # Disable python warnings for script call.
    if sys.platform != 'win32':
        command = 'export PYTHONWARNINGS="" && {}'.format(command)
    if VERBOSE:
        print('command {}'.format(command))
    proc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE)
    std_out, std_err = proc.communicate()
    exitcode = proc.returncode

    HELP_DICT[cmd] = std_out

    if six.PY3:
        std_out = std_out.decode()
        std_err = std_err.decode()

    if exitcode:
        raise RuntimeError('Error: Shell execution of command {!r} failed with '
                           'rc={}: {}'.format(command, exitcode, std_err))
    if std_err:
        raise RuntimeError("Error: Unexpected stderr from command {!r}:\n"
                           "{}".format(command, std_err))

    # Split stdout into list of lines
    lines = std_out.split('\n')

    # get first word of all lines after line containing 'Commands:'
    group_list = []
    group_state = False
    for line in lines:
        if group_state and line:
            # split line into list of words and get first word as command
            words = line.split()
            group_list.append(words[0])

        # test for line that matchs the word Commands
        if line.strip() == 'Commands:':
            group_state = True
    return group_list


def get_subgroup_names(group_name, script_cmd, script_name):
    """
    Get all the commands for the help_group_name defined on input.
    Executes script and extracts groups after line with 'Commands'
    """
    subcmds_list = get_subcmd_group_names(script_cmd, script_name, group_name)
    space = ' ' if group_name else ''

    return ['{}{}{}'.format(group_name, space, name) for name in subcmds_list]


def create_help_cmd_list(script_cmd, script_name):
    """
    Create the command list.
    """
    # Result list of assembled help subcmds
    help_groups_result = []
    # start with empty group, the top level (i.e. pywbemcli --help).
    # This is list of names to process and is extended as we process
    # each group.
    group_names = [""]

    help_groups_result.extend(group_names)
    for name in group_names:
        return_cmds = get_subgroup_names(name, script_cmd, script_name)
        help_groups_result.extend(return_cmds)
        # extend input list with returned assembled groups
        group_names.extend(return_cmds)
    # sort to match order of click
    help_groups_result.sort()
    if USE_RST:
        print(rst_headline("{} Help Command Details".format(script_name), 2))
        if script_name == 'pywbemcli':
            print('\nThis section shows the help text for each {} '
                  'command group and command.\n'.format(script_name))
        else:  # 'pywbemlistener'
            print('\nThis section shows the help text for each {} '
                  'command.\n'.format(script_name))

    for name in help_groups_result:
        command = '{} {}'.format(script_name, name)
        command_help = '{} {} --help'.format(script_name, name)
        out = HELP_DICT[name]
        if USE_RST:
            level = len(name.split())  # 0: top, 1: group, 2: command
            if script_name == 'pywbemcli':
                if level == 0:
                    line = 'Help text for ``{}``:'.format(script_name)
                elif level == 1 and name not in ('repl', 'help', 'docs'):
                    line = 'Help text for ``{}`` (see :ref:`{} command ' \
                    'group`):'.format(command, name)
                else:
                    line = 'Help text for ``{}`` (see :ref:`{} command`):' \
                        .format(command, name)
            else:  # 'pywbemlistener'
                if level == 0:
                    line = 'Help text for ``{}``:'.format(script_name)
                else:  # level == 1
                    line = 'Help text for ``{}`` (see :ref:`{} {} command`):'. \
                    format(command, script_name, name)
            if level > 0:
                # Don't generate section header for top level
                print(rst_headline(command_help, 2 + level))
            print('\n\n{}\n\n'.format(line))
            print_rst_verbatum_text(out.decode())
        else:
            print('{}\n{} command: {}'
                  .format(('=' * 50), script_name, command_help))
            print(out.decode())

    return help_groups_result


if __name__ == '__main__':
    # Verify that the script exists. Executing with --help loads click
    # script generates help and exits.
    check_cmd = '{} --help'.format(SCRIPT_CMD)
    rc, msg = cmd_exists(check_cmd)
    if rc != 0:
        print("Error: Shell execution of {!r} returns rc={}: {}"
              .format(check_cmd, rc, msg), file=sys.stderr)
        sys.exit(1)
    create_help_cmd_list(SCRIPT_CMD, SCRIPT_NAME)
