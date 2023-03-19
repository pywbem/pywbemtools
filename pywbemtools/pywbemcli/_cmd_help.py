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

from .._click_extensions import GENERAL_OPTS_TXT, TabCompleteArgument

from .pywbemcli import cli
from .._options import add_options, help_option
from ._cmd_instance import HELP_INSTANCENAME_MSG
from .._common_cmd_actions import help_subjects_action


def help_arg_subject_shell_completer(ctx, param, incomplete):
    # pylint: disable=unused-argument
    """
    Shell complete function for the help subjects argument.  This function is
    called if <TAB> is entered from terminal as part of the value of the
    -help <subject>.  It returns all subject names that
    start with the string in incomplete.
    """
    subject_keys = PYWBEMCLI_HELP_SUBJECTS_DICT.keys()
    # pylint: disable=no-member
    return [click.shell_completion.CompletionItem(name) for name in
            subject_keys if name.startswith(incomplete)]


@cli.command('help', options_metavar=GENERAL_OPTS_TXT)
@click.argument('subject', type=str,
                metavar='SUBJECT',
                cls=TabCompleteArgument,
                shell_complete=help_arg_subject_shell_completer,
                required=False)  # pylint: disable=no-member
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
    click.echo(help_subjects_action(ctx.obj, subject,
                                    PYWBEMCLI_HELP_SUBJECTS_DICT))


# pylint: disable=invalid-name
activate_shell_help_msg = '''
Pywbemcli shell tab-completion must be activated after installation by notifying
the shell before the <TAB> becomes active when entering a pywbemcli command in
the shell.

Tab-completion is only available for certain shells including: bash (version
4.4 or greater), zsh, and fish shells since pywbemcli defines the completer
script specifically for each shell.

Activation of pywbemcli involves the following but with different formats for
each shell type:

1. Getting from pywbemcli the body of a completion script that defines
   activation for the shell. This is done by executing the script statement
     '_PYWBEMCLI_COMPLETE=<shell>_source pywbemcli'
     where <shell> can be 'bash', 'zsh', or 'fish'.
    This causes the shell to call back to pywbemcli with '_PYEBEMCLI_COMPLETE'
    and '<shell>_source' arguments wherein pywbemcli returns the completion
    script.
2. Setting up the shell of this completion script by either:
   * an 'eval' statement in the terminal startup
     (ex. .bashrc ) that defines the completion script or,
   * Creating a completion script file and sourcing that file later to activate.

The 'eval' statement for each of the shells supported is as follows and can
be inserted into the corresponding shell startup script defined below.

NOTE: For Python 2, replace '<shell-name>_source' with 'source_<shell-name>`.

=====  ============  ===========================================================
shell  startup file  eval command
=====  ============  ===========================================================
bash  ~/.bashrc      eval "$(_PYWBEMCLI_COMPLETE=bash_source pywbemcli)"
zsh   ~/.zshrc       eval "$(_PYWBEMCLI_COMPLETE=zsh_source pywbemcli)"
fish  ~/.config/fish/completions/foo-bar.fish
                     eval "$(env _PYWBEMCLI_COMPLETE=fish_source pywbemcli)"
=====  ===========  ===========================================================

Activate pywbemcli tab-completion as follows:

  1. Edit the eval command in the startup file or
  2. Close the file and restart the terminal or
  3. Test existence of tab-completion by:
     a. Test completion with a command such as "pywbemcli cl<TAB> which should
        complete the "class" command group name.
     b. In bash executing "complete -p pywbemcli". An entry for pywbemcli must
        exist for pywbemcli as follows:

          ``complete -o nosort -F _pywbemcli_completion pywbemcli``

Executing ``eval`` directly in the shell startup file has the issue that the
pywbemcli executable location must be known when opening a terminal . This may
not be consistent with executing pywbemcli in virtual environments.

To activate tab-completion using a completion file execute the command defined
below for the desired shell to create the completion script for pywbemcli
in  a file (ex.~/pywbemcli-complete.bash). This command requires that that
pywbemcli be available. The file name is arbitrary.
=====  =====================================================================
shell  completion file creating command
=====  =====================================================================
bash   _PYWBEMCLI_COMPLETE=bash_source pywbemcli > ~/.pywbemcli-complete.bash
zsh    _PYWBEMCLI_COMPLETE=zsh_source pywbemcli > ~/.pywbemcli-complete.zsh
fish   _PYWBEMCLI_COMPLETE=fish_source pywbemcli >
          ~/.config/fish/completions/pywbemcli.fish
=====  =====================================================================

Once the completion script file is created, pywbemcli tab-completion can be
activated by sourcing this script (ex 'source ~/.pywbemcli-complete.bash')
upon shell startup. This does not actually call pywbemcli.  This can be done a
number of different ways, for example:

* Include the sourcing statement in the shell startup script (ex. ~/.bashrc)
* Execute the statement as part of the startup of a virtual envrionment.
* Manually execute the sourcing statement when required before calling pywbemcli
'''
# pylint: enable=invalid-name

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

# pylint: disable=invalid-name
tab_completion_help_msg = """
Tab completion is always available in the interactive mode (see help repl).
Tab completion in the command mode, when activated,

Tab completion for option values and arguments exists when the data is local.
It is not provided for option values and arguments where access to a WBEM
server is required.

Tab completion  is available for:

* the command group names
* the command names
* the option names
* The values of some general options including:
    * --name
    * --mock-server
    * --use-pull
    * --connections-file
    * --keyfile
    * --certfile
    * --outputformat
* the values of some arguements
    * help <subject> argument

When tab completion is not available for an argument or option value, entering
<TAB> does nothing.
"""


###########################################################################
#
#  Table of subjects
#
###########################################################################

# FUTURE: Other subjects: connection file, command structure, checkpointing
# of mock server definition, arguments and options, etc.
PYWBEMCLI_HELP_SUBJECTS_DICT = {
    "repl": ("Using the repl command", repl_help_msg),
    'activate': ("Activating shell tab completion",
                 activate_shell_help_msg),
    'instancename': ('InstanceName parameter in instance cmd group',
                     HELP_INSTANCENAME_MSG),
    'tab-completion': ("Where tab completion is provided by pywbemcli",
                       tab_completion_help_msg),
}
