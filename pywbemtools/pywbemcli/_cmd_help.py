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
Click Command definition for the help subjects command which shows the
test of help subjects defined in a help_subjects_dict.

Note that this is a command and not a command group.

The help text for each subject may be in this file or in the file associated
with the particular subject.
"""

from __future__ import absolute_import, print_function


import click

from .._click_extensions import GENERAL_OPTS_TXT

from .pywbemcli import cli
from .._options import add_options, help_option
from ._cmd_instance import HELP_INSTANCENAME_MSG
from .._output_formatting import validate_output_format, format_table

# FUTURE: add the tab-completion function for the subject argument


@cli.command('help', options_metavar=GENERAL_OPTS_TXT)
@click.argument('subject', type=str, metavar='SUBJECT', required=False)
@add_options(help_option)
@click.pass_context
def help_subjects(ctx, subject):   # pylint: disable=unused-argument
    """
    Show help for pywbemcli subjects.

    Show help for specific pywbemcli subjects.  This is in addition to the
    help messages that are available with the -h or --help option for every
    command group and command in pywbemcli. It helps document pywbemcli
    subjects that are more general than specific commands and configuration
    subjects that do not have specific commands

    If there is no argument provided, outputs a list and summary of the
    existing help subjects.

    If an argument is provided, it outputs the help for the subject(s) defined
    by the argument.
    """
    subjects = sorted(list(HELP_SUBJECTS_DICT.keys()))

    # If there is no subject argument, output a table of all of the subjects and
    # short descriptions.

    if not subject:
        # max_subject_len = len(max(subjects, key=len))
        rows = []
        for name in subjects:
            subject = HELP_SUBJECTS_DICT[name]
            rows.append([name, subject[0]])

        output_format = validate_output_format(ctx.obj.output_format, 'TABLE')
        click.echo(format_table(rows, ("subject name", "subject description"),
                                title='Help subjects',
                                table_format=output_format))

        return

    # If a subject exists, output the help for that subject
    if subject in HELP_SUBJECTS_DICT:
        click.echo("{0} - {1}\n{2}".
                   format(subject,
                          HELP_SUBJECTS_DICT[subject][0],
                          HELP_SUBJECTS_DICT[subject][1]))
    else:
        raise click.ClickException("{} is not a subject in the subjects help".
                                   format(subject))


# FUTURE: Move this to new module along with repl command. Every cmd should
#         be in separate module with its data.
# pylint: disable=invalid-name
repl_help_msg = """
In the interactive mode pywbem returns control to a terminal. General
options, commands, and command options may be entered. Pywbemcli remains in the
interactive mode until terminated by <CTRL-D>, :q, :quit,  or :exit.

Pywbemcli enters interactive (repl) mode when started without a command.
General options entered in the interactive mode are only active for the current
command where upon the command line general options are restored.

The prompt for the interactive mode is pywbemcli$

Tab-completion <TAB> and autosuggestion help (suggest completions based on the
pywbemcli history file) are always active in the interactive mode.

The following can be entered in interactive (repl) mode:

  COMMAND                     Execute pywbemcli command COMMAND.
  !SHELL-CMD                  Execute shell command SHELL-CMD.
  <CTRL-D>, :q, :quit, :exit  Exit interactive mode.
  <CTRL-r>  <search string>   Search pywbemcli command history file.
                              Can be used with <UP>, <DOWN>
                              to display commands that match the search string.
                              Editing the search string updates the search.
  <TAB>                       Tab completion (can be used anywhere on cmd line).
  -h, --help                  Show pywbemcli general help message, including a
                              list of pywbemcli commands.
  COMMAND --help              Show help message for pywbemcli command COMMAND.
  help                        Show help subjects.
  help repl                   Show help for the repl mode.
  :?, :h, :help               Show help message about interactive mode.
  <UP>, <DOWN>                Scroll through pwbemcli command history.

  COMMAND: May be two words (class enumerate) for commands that are within
  a group or a single word for special commands like `repl` that are not in
  a group.

Example:
   pywbemcli -n mock1

   ... pywbemcli is now in the interactive mode

   pywbemcli$ class enumerate
      . . .  Returns classes enumerated.

   pywbemcli$ class get blah
      . . . Returns mof for class blah if it exists.

   pywbemcli$ -v namespace list
      . . . Gets namespaces for connection named mock1 but with verbose output

      . . . Returns to non-verbose output for next command
   pywbemcli$
"""  # pylint: enable=invalid-name


# FUTURE: Other subjects: connection file, command structure, checkpointing
# of mock server definition, arguments and options, etc.
HELP_SUBJECTS_DICT = {
    "repl": ("Using the repl command", repl_help_msg),
    # 'activate': ("Activating shell tab completion",
    #             tab_completion_help_msg),
    'instancename': ('InstanceName parameter in instance cmd group',
                     HELP_INSTANCENAME_MSG)
}
