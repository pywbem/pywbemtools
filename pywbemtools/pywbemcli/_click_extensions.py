"""
This file contains extensions to Click specifically for pywbemcli
"""
import sys
from collections import OrderedDict

import click

from ._common import GENERAL_OPTS_TXT, CMD_OPTS_TXT


class PywbemcliGroup(click.Group):
    """
    Extend Click Group class to:
    1.  Order the display of commands within the help.
        The commands are ordered in the order that their definitions
        appears in the source code for each command group.
    This extension has a general name because it may be used for more than
    one extension to the Click.Group class.

    2. Force use of our method pywbemcli_format_usage rather than
       the click define Command.format_usage()

    It is used on all group decorators (@click.group(...)) except for the
    top level in pywbemcli which uses the PywbemcliTopGroup class.
    """

    # Use ordered dictionary to sort commands by their order defined in the
    # _cmd_... source file.
    def __init__(self, name=None, commands=None, **attrs):
        """
        Use OrderedDict to keep order commands inserted into command dict.
        Only required for Python versions that do not order dictionaries.
        Must be set after calling superclass __inits_ because click forces
        {} for this variable even if user were to set commands to OrderedDict
        """
        super(PywbemcliGroup, self).__init__(name, commands, **attrs)

        if sys.version_info < (3, 6):
            self.commands = commands or OrderedDict()

        # Replace Click.Command.format_usage with local version
        click.core.Command.format_usage = pywbemcli_format_usage
        click.core.Command.format_options = pywbemcli_format_options

    def list_commands(self, ctx):
        """
        Replace click.list_commands to eliminate the sort of cmd names.
        """
        return self.commands.keys()


class PywbemcliTopGroup(click.Group):
    """
    Extensions to be used with the top level help (pywbemcli --help)

    Extend Click Group class to:
    1.  Order the display of the commands and command groups in the top level
        help output to sort and then put names defined in the predefined_list
        at the end of the list of commands/groups. Since ordering of the top
        level cannot be tied to order commands are inserted in list, we elected
        to just move the generic ones to the end of the list.

    This extension has a general name because it may be used for more than
    one extension to the Click.Group class.
    """

    def __init__(self, name=None, commands=None, **attrs):
        """
        Use OrderedDict to keep order commands inserted into command dict.
        Only required for Python versions that do not order dictionaries.
        Must be set after calling superclass __inits_ because click forces
        {} for this variable even if user were to set commands to OrderedDict
        """
        super(PywbemcliTopGroup, self).__init__(name, commands, **attrs)

        # Replace Click.Command.format_options with local version
        click.core.Command.format_options = pywbemcli_format_options

    def list_commands(self, ctx):
        """
        Order The top level commands by sorting and then moving any commands
        defined in  move_to_end list to the end of the list.  This is
        the class override for click.Group ONLY with the top group, the
        click startup group in pywbemcli because in reorders the commands
        display specifically as we want them for pywbemcli.
        """
        # tuple of commands to move to bottom after sort
        move_to_end = ('connection', 'help', 'repl')

        # Sort because thier is no particular order for the groups
        cmd_list = sorted(self.commands.keys())
        pop_count = 0
        # reorder list so the move_to_end list commands are at bottom
        for i in range(len(cmd_list)):
            if cmd_list[i - pop_count] in move_to_end:
                cmd_list.append(cmd_list.pop(i - pop_count))
                pop_count += 1
        return cmd_list


class PywbemcliCommand(click.Command):
    """
    Modify the command usage formatter to show the commands in a format
    that fits how we use the tool. This should be the cls= argument
    for all pywbemcli command decorators (i.e. `@class_group.command(`).
    """

    def format_usage(self, ctx, formatter):
        """
        Replaces click.Command.format_usage
        """
        pieces = self.collect_usage_pieces(ctx)
        cmd_paths = ctx.command_path.split()
        # Reorder pieces to order GENERAL_OPTS_TXT, <cmd> ...
        new_pieces = [GENERAL_OPTS_TXT] + cmd_paths[1:] + pieces[1:] \
            + [pieces[0]]
        formatter.write_usage(cmd_paths[0], " ".join(new_pieces))


def pywbemcli_format_usage(self, ctx, formatter):
    """
    Replaces click.Command.format_usage in the fixes for click.Group
    """
    pieces = self.collect_usage_pieces(ctx)
    cmd_paths = ctx.command_path.split()

    # cmd_path is [<appname>, group, cmd]
    # If cmd_path has multiple components we are showing
    # app name, CMDGRP <cmd>. Break out CMDGRP and <cmd>
    # and reinsert after pieces[0] (the app name)
    if len(cmd_paths) > 1:
        new_pieces = [pieces[0]] + cmd_paths[1:] + pieces[1:]
        formatter.write_usage(cmd_paths[0], " ".join(new_pieces))
    else:
        formatter.write_usage(ctx.command_path, " ".join(pieces))


def pywbemcli_format_options(self, ctx, formatter):
    """
    Writes all the options into the formatter if they exist.
    """
    opts = []
    cmds_len = len(ctx.command_path.split())

    # If group or command level, use CMD_OPTS_TXT
    options_title = CMD_OPTS_TXT if cmds_len > 1 else GENERAL_OPTS_TXT
    # Cvt to string of words with first char of each word capitalized
    options_title = options_title[1:-1].lower().replace('-', " ").title()

    for param in self.get_params(ctx):
        rv = param.get_help_record(ctx)
        if rv is not None:
            opts.append(rv)

    if opts:
        with formatter.section(options_title):
            formatter.write_dl(opts)
