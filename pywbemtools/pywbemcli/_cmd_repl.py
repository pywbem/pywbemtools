# (C) Copyright 2023 IBM Corp.
# (C) Copyright 2023 Inova Development Inc.
# All Rights Reserved
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""
Click repl command. This command initates the pywbemcli interactive mode where
commands can be entered within an existing general options context.

This coded depends on the click-repl package as infrastructure
"""

from __future__ import absolute_import, print_function

import os
from collections import deque

import click

from prompt_toolkit.history import FileHistory
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory

from click_repl import Repl
import click_repl
from click_repl._internal_cmds import InternalCommandSystem
from prompt_toolkit.completion import Completion
from click_repl.completer import ClickCompleter
from click_repl.utils import join_options
from click_repl import parser

from .pywbemcli import cli

from .._click_extensions import GENERAL_OPTS_TXT
from .._options import add_options, help_option

from .config import PYWBEMCLI_PROMPT, PYWBEMCLI_HISTORY_FILE, \
    USE_AUTOSUGGEST

from .._utils import pywbemtools_warn


class CustomClickCompleter(ClickCompleter):
    def get_completion_for_command_args(self, ctx, command, args, incomplete):
        current_param = None

        opt_names = []
        for param in command.params:
            if getattr(param, "hidden", False):
                continue

            opts = param.opts + param.secondary_opts
            if any(i in args[param.nargs*-1:] for i in opts):
                current_param = param
                break

            opts_with_incomplete_prefix = [
                opt for opt in opts if opt.startswith(incomplete)
            ]

            if (
                (  # If param is a bool flag, and its already in args
                    getattr(param, "is_bool_flag", False)
                    and any(i in args for i in opts)
                )
                # Or the param is called recently within its nargs length
                or not opts_with_incomplete_prefix
            ):
                continue

            display_meta = getattr(param, "help", "")

            # display = param.metavar or option
            opts, sep = join_options(opts)
            display = sep.join(opts_with_incomplete_prefix)

            if not (getattr(param, "count", False) or param.default is None):
                display += f" [Default={param.default}]"

            opt_names.append(
                Completion(
                    min(opts, key=len),
                    -len(incomplete),
                    display=display,
                    display_meta=display_meta,
                    style=self.styles["option"],
                )
            )

        if current_param is None:
            params_list = deque(
                i for i in command.params if isinstance(i, click.Argument)
            )
            minus_one_param = None

            while params_list:
                # Replaced with code
                # param = _fetch(params_list, minus_one_param)

                try:
                    if minus_one_param is None:
                        param = params_list.deque.popleft()
                    else:
                        param = params_list.deque.pop()
                except IndexError as ie:
                    print(f'Index error {ie}, param {param}')

                if param is None:
                    break

                if param.nargs == -1:
                    minus_one_param = param

                elif ctx.params[param.name] is None:  # type: ignore[index]
                    current_param = param
                    break

            current_param = minus_one_param

        current_param_is_None = current_param is None
        if current_param_is_None or isinstance(current_param, click.Argument):
            yield from opt_names

        if not (
            current_param_is_None or getattr(current_param, "hidden", False)
        ):
            yield from self.get_completion_from_params(
                ctx, current_param, args, incomplete
            )

    def get_completions_for_command(self, ctx, state, args, incomplete):
        breakpoint()
        current_group = state.current_group
        current_command = state.current_command

        yield from self.get_completion_for_command_args(
            ctx,
            current_command if current_command else self.cli,
            args,
            incomplete
        )

        if not current_command:
            for name in current_group.list_commands(ctx):
                command = current_group.get_command(ctx, name)
                if getattr(command, "hidden", False):
                    continue

                elif name.startswith(incomplete):
                    yield Completion(
                        name,
                        -len(incomplete),
                        display_meta=getattr(command, "short_help", ""),
                    )


class MyRepl(Repl):
    def execute_click_cmds(self, command: str) -> None:
        args = parser.split_arg_string(command)
        with self.group.make_context('', args, parent=self.group_ctx) as ctx:
            self.group.invoke(ctx)
            ctx.exit()


class InvalidConnectionFile(Warning):
    """
    Indicates that invalid connection file in startup of interactive mode.
    """
    pass


original_resolve_context = click_repl.utils._resolve_context


def new_func(ctx, args):
    cli = ctx.command
    ctx = cli.make_context("", args.copy(), resilient_parsing=True)
    args = ctx.protected_args + ctx.args
    return original_resolve_context(ctx, args)


_resolve_context = new_func


@cli.command('repl', options_metavar=GENERAL_OPTS_TXT)
@add_options(help_option)
@click.pass_context
def repl(ctx):
    """
    Enter interactive mode (default).

    Enter the interactive mode where pywbemcli commands can be entered
    interactively. The prompt is changed to 'pywbemcli>'.

    <COMMAND> <COMMAND OPTIONS> - Execute pywbemcli command COMMAND

    <GENERAL_OPTIONS> <COMMAND> <COMMAND_OPTIONS> - Execute command with
    general options.  General options set here exist only for the current
    command.

    -h, --help - Show pywbemcli general help message, including a
                                  list of pywbemcli commands.
    COMMAND -h, --help - Show help message for pywbemcli command COMMAND.

    !SHELL-CMD - Execute shell command SHELL-CMD

    Pywbemcli termination - <CTRL-D>, :q, :quit, :exit

    Command history is supported. The command history is stored in a file
    ~/.pywbemcli_history.

    <UP>, <DOWN> - Scroll through pwbemcli command history.

    <CTRL-r> <search string> - initiate an interactive
    search of the pywbemcli history file. Can be used with <UP>, <DOWN>
    to display commands that match the search string.
    Editing the search string updates the search.

    <TAB> - tab completion for current command line
    (can be used anywhere in command)

    Interactive mode also includes an autosuggest feature that makes
    suggestions from the command history as the command the user types in the
    command and options.
    """
    breakpoint()
    history_file = PYWBEMCLI_HISTORY_FILE
    if history_file.startswith('~'):
        history_file = os.path.expanduser(history_file)

    click.echo("Enter 'help repl' for help, <CTRL-D> or ':q' "
               "to exit pywbemcli or <CTRL-r> to search history, ")

    if not ctx.obj.connections_repo.file_exists():
        pywbemtools_warn(
            "Connections file: '{}' does not exist. Server and connection "
            "commands will not work.".
            format(ctx.obj.connections_repo.connections_file),
            InvalidConnectionFile, stacklevel=0)

    # And inside the repl command function
    prompt_kwargs = {
        'message': PYWBEMCLI_PROMPT,
        'history': FileHistory(history_file),
        # InternalCommandSystem() is just to enable the internal commands in
        # the repl
        "completer": CustomClickCompleter(ctx, InternalCommandSystem()),
        'validator': None,
        'bottom_toolbar': None,
    }

    if USE_AUTOSUGGEST:
        prompt_kwargs['auto_suggest'] = AutoSuggestFromHistory()

    click_repl.repl(ctx, prompt_kwargs=prompt_kwargs, repl_cls=MyRepl)
