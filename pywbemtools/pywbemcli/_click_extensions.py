"""
This file contains extensions to Click specifically for pywbemcli
"""
import sys
from collections import OrderedDict
import click


class PywbemcliGroup(click.Group):
    """
    Extend Click Group class to:
    1.  Order the display of commands within the help.
        The commands are ordered in the order that their definitions
        appears in the source code for each command group.
    This extension has a general name because it may be used for more than
    one extension to the Click.Group class.
    """

    # Use ordered dictionary to sort commands by their order defined in the
    # _cmd_... source file.
    def __init__(self, name=None, commands=None, **attrs):
        """
        Use OrderedDict to keep order commands inserted into command dict.
        Only required for Python versions that do not order dictionaries.
        Must be set after calling superclass __inits_ because click forces
        {} even if user were to set commands to OrderedDict
        """
        super(PywbemcliGroup, self).__init__(name, commands, **attrs)
        #: the registered subcommands by their exported names.
        if sys.version_info < (3, 6):
            self.commands = commands or OrderedDict()

    def list_commands(self, ctx):
        """
        Replace list_commands to eliminate the sort.
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

    def list_commands(self, ctx):
        """
        Order The top level commands by sorting and then moving any commands
        defined in  move_to_end list to the end of the list.
        """
        # tuple of commands to move to bottom after sort
        move_to_end = ('connection', 'help', 'repl')

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
    that fits how we use the tool
    """

    def format_usage(self, ctx, formatter):
        """
        """
        pieces = self.collect_usage_pieces(ctx)
        cmd_paths = ctx.command_path.split()

        # If cmd_path has multiple components we are showing
        # app name, CMDGRP <cmd>. Break out CMDGRP and <cmd>
        # and reinsert after pieces[0] (the app name)
        if len(cmd_path) > 1:
            new_pieces = [pieces[0]] + cmd_paths[1:] + pieces[1:]
            formatter.write_usage(cmds[0], " ".join(new_pieces))
        else:
            formatter.write_usage(ctx.command_path, " ".join(pieces))
