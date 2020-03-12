"""
This file contains extensions to Click
"""

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
        Use OrderedDict to keep order commands inserted into command dict
        """
        print('PYWBEMCI_INIT %s %s' % (name, commands))
        print('attrs %s' % attrs)
        if commands is None:
            commands = OrderedDict()
        elif not isinstance(commands, OrderedDict):
            print('PYWBEMCLI INIT pre commands %s' % commands)
            commands = OrderedDict(commands)
        click.Group.__init__(self, name=name, commands=commands, **attrs)

    def list_commands(self, ctx):
        """
        Replace list_commands to eliminate the sorting
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
        print("LIST_COMMANDS %s" % self.commands.keys())
        # tuple of commands to move to bottom after sort
        move_to_end = ('connection', 'help', 'repl')

        cmd_list = sorted(self.commands.keys())
        pop_count = 0
        # reorder list so the move_to_end list commands are at bottom
        for i in range(len(cmd_list)):
            if cmd_list[i - pop_count] in move_to_end:
                cmd_list.append(cmd_list.pop(i - pop_count))
                pop_count += 1
        print('RETURNS %s' % cmd_list)
        return cmd_list
