"""
This file contains extensions to Click for pywbemtools.
"""

import sys
from collections import OrderedDict
import packaging.version

import click

# Definitions of the components of the help usage line
GENERAL_OPTS_TXT = '[GENERAL-OPTIONS]'
CMD_OPTS_TXT = '[COMMAND-OPTIONS]'
SUBCMD_HELP_TXT = "COMMAND [ARGS] " + CMD_OPTS_TXT

# Click version as a tuple
CLICK_VERSION = packaging.version.parse(click.__version__).release


class PywbemtoolsGroup(click.Group):
    """
    Extend Click Group class to:

    1.  Order the display of commands within the help.
        The commands are ordered in the order that their definitions
        appears in the source code for each command group.

    2. Force use of our method pywbemtools_format_usage rather than
       the click define Command.format_usage()

    This class is used by specifying it for the 'cls' argument on those
    groups that are not the top level group, for example:

        @cli.group('class', cls=PywbemtoolsGroup, ...)
    """

    def __init__(self, name=None, commands=None, **attrs):
        """
        Use OrderedDict to keep order commands inserted into command dict.
        Only required for Python versions that do not order dictionaries.
        Must be set after calling superclass __inits_ because click forces
        {} for this variable even if user were to set commands to OrderedDict
        """
        super(PywbemtoolsGroup, self).__init__(name, commands, **attrs)

        if sys.version_info < (3, 6):
            self.commands = commands or OrderedDict()

        # Replace Click.Command.format_usage with local version
        click.core.Command.format_usage = pywbemtools_format_usage
        click.core.Command.format_options = pywbemtools_format_options

    def list_commands(self, ctx):
        """
        Replace click.list_commands to eliminate the sort of cmd names.
        """
        return self.commands.keys()


class PywbemtoolsTopGroup(click.Group):
    """
    Extensions to be used with the top level help.

    Extend Click Group class to:

    1.  Order the display of the commands and command groups in the top level
        help output to sort and then put names defined in the predefined_list
        at the end of the list of commands/groups. Since ordering of the top
        level cannot be tied to order commands are inserted in list, we elected
        to just move the generic ones to the end of the list.

    This class is used by specifying it for the 'cls' argument on the top
    level group, for example:

        @click.group(cls=PywbemtoolsTopGroup, ...)
    """

    def __init__(self, name=None, commands=None, move_to_end=None, **attrs):
        """
        Use OrderedDict to keep order commands inserted into command dict.
        Only required for Python versions that do not order dictionaries.
        Must be set after calling superclass __inits_ because click forces
        {} for this variable even if user were to set commands to OrderedDict.

        Parameters:

          move_to_end (list): List of to level command/group names that will be
            moved to the end of the list after sorting it, or `None` for not
            moving any.
        """
        self.move_to_end = move_to_end or []
        super(PywbemtoolsTopGroup, self).__init__(name, commands, **attrs)

        # Replace Click.Command.format_options with local version
        click.core.Command.format_options = pywbemtools_format_options

    def list_commands(self, ctx):
        """
        Order the top level commands by sorting and then moving any commands
        defined in move_to_end list to the end of the list.

        This happens only for the top level commands/groups because this is the
        class override for click.Group ONLY with the top group.
        """
        # Sort because thier is no particular order for the groups
        cmd_list = sorted(self.commands.keys())
        pop_count = 0
        # reorder list so the move_to_end list commands are at bottom
        for i in range(len(cmd_list)):
            if cmd_list[i - pop_count] in self.move_to_end:
                cmd_list.append(cmd_list.pop(i - pop_count))
                pop_count += 1
        return cmd_list

    def __call__(self, *args, **kwargs):
        """
        This method is called once for each execution of the pywbemtools
        command, by the generated command entry point code (e.g. the 'pywbemcli'
        script).

        This method extends the default behavior by disabling wildcard expansion
        on Windows, when using Click 8.0.1 or higher (that is the version which
        introduced this argument).
        """
        if CLICK_VERSION >= (8, 0, 1):
            kwargs = dict(kwargs)
            kwargs['windows_expand_args'] = False
        return self.main(*args, **kwargs)


class PywbemtoolsCommand(click.Command):
    """
    Modify the command usage formatter to show the commands in a format
    that fits how we use the tool.

    This class is used by specifying it for the 'cls' argument on all command
    decorators, for example:

        @class_group.command('enumerate', cls=PywbemtoolsCommand, ...)
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


def pywbemtools_format_usage(self, ctx, formatter):
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


def pywbemtools_format_options(self, ctx, formatter):
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


# The following MutuallyExclusiveOption originated with a number of
# discussions on stack overflow and a github gist at
# https://gist.github.com/stanchan/bce1c2d030c76fe9223b5ff6ad0f03db

class MutuallyExclusiveOption(click.Option):
    """
    This class subclasses Click option to allow defining mutually exclusive
    options.

    An option is defined as mutually exclusive with another option on the
    same command if the two options cannot be used simultaneously.
    With this class, mutually exclusive options are defined by using this
    class in place of the option class (Set the cls parameter to
    cls=MutuallyExclusiveOption) and the parameter mutually_exclusive set
    in the option defining the options with which this one is mutually
    exclusive. A boolean parameter show_mutually_exclusive can be set to
    True to add the text:
    Conflicting options: <option_name> is mutually exclusive with "
    "options: (<list of mutually exclusive options>)

    Example:

    @option('--first-option', cls=MutuallyExclusiveOption,
        help="This option is mutually exclusieve with other-arg.",
        mutually_exclusive=["second-option"])
    @option('--second-option',
        cls=MutuallyExclusiveOption,
        help="second-option blah.",
        mutually_exclusive=["first-option"],
        show_mutually_exclusive=True)

    This simple extension is used with pywbemcli now because the alternative
    (click contrib options groups) only works with python 3.6+
    """
    def __init__(self, *args, **kwargs):
        # Remove the mutually exclusive option parameters from kwargs
        self.mutually_exclusive = kwargs.pop('mutually_exclusive', [])

        # Get show_mutually_exclusive flag or True
        show_mutually_exclusive_flag = kwargs.pop('show_mutually_exclusive',
                                                  True)

        # If flag set, add comment to help
        if self.mutually_exclusive and show_mutually_exclusive_flag:
            help_txt = kwargs.get('help', '')
            kwargs['help'] = "{0} This option is mutually exclusive with " \
                "options: ({1}).". \
                format(help_txt, self._mutually_exclusive_display())

        super(MutuallyExclusiveOption, self).__init__(*args, **kwargs)

    def handle_parse_result(self, ctx, opts, args):
        """
        If this is mutually exclusive opt and the list intersects with
        the options in the command, generate click.UsageError
        """
        me_internal = set([i.replace('-', '_') for i in
                           self.mutually_exclusive])
        if me_internal.intersection(opts) and self.name in opts:
            raise click.UsageError(
                "Conflicting options: `{0}` is mutually exclusive with "
                "options: ({1}).".
                format(self.name.replace('_', '-'),
                       self._mutually_exclusive_display()))

        return super(MutuallyExclusiveOption, self).handle_parse_result(
            ctx, opts, args)

    def _mutually_exclusive_display(self):
        """Format/sort list for display."""
        return ', '.join(
            sorted(["--{0}".format(i) for i in self.mutually_exclusive]))
