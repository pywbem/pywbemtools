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

from .pywbemlistener import cli
from .._options import add_options, help_option
from .._common_cmd_actions import help_subjects_action


def help_arg_subject_shell_completer(ctx, param, incomplete):
    # pylint: disable=unused-argument
    """
    Shell complete function for the help subjects argument.  This function is
    called if <TAB> is entered from terminal as part of the value of the
    -help <subject>.  It returns all subject names that
    start with the string in incomplete.
    """
    subject_keys = PYWBEMLISTENER_HELP_SUBJECTS_DICT.keys()
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
    Show help for pywbemlistener subjects.

    Show help for specific pywbemlistener subjects.  This is in addition to the
    help messages that are available with the -h or --help option for every
    command group and command in pywbemlistener. It helps document
    pywbemlistener subjects that are more general than specific commands and
    configuration subjects that do not have specific commands

    If there is no argument provided, outputs a list and summary of the
    existing help subjects.

    If an argument is provided, it outputs the help for the subject(s) defined
    by the argument.
    """
    click.echo(help_subjects_action(ctx.obj, subject,
                                    PYWBEMLISTENER_HELP_SUBJECTS_DICT))


# pylint: disable=invalid-name,
activate_shell_help_msg = '''
Pywbemlistener includes tab-completion capability for all commands for certain
shell types program being used by the command line terminal.

Tab-completion is active only when it is activated by
notifying the command shell of the pywbemlistener tab-completion
characteristics. Further, it is only usable with those shells that include
tab-completion as part of the shell functionality.  On Linux based systems this
includes shells like bash (version 4.0 or greater), zsh, and fish.

Activation of pywbemlistener involves the following but with different formats
for each shell type:

* Getting from pywbemlistener the body of a completion script for the shell to
  be activated. This is done by executing a script statement of form
  ``_pywbemlistener_COMPLETE=bash_source pywbemlistener``.
* Notifying the shell of this completion script with an eval statement or
  saving the script and notifying the shell later by sourcing the resulting
  completion script file.

Tab-completion can be activated either by:

* Installing the activation script with an eval statement into .bashrc
* Creating a completion script file and sourcing that file at a later time.

The ``eval`` statement for each of the shells supported is as follows and can
be inserted into the corresponding shell startup script defined below.

NOTE: For Python 2, replace the <shell-name>_source with source_<shell-name>

=====  ============  ===========================================================
shell  startup file  eval command
=====  ============  ===========================================================
bash  ~/.bashrc      eval "$(_PYWBEMLISTENER_COMPLETE=
                           bash_source pywbemlistener)"
zsh   ~/.zshrc       eval "$(_PYWBEMLISTENER_COMPLETE=
                           zsh_source pywbemlistener)"
fish  ~/.config/fish/completions/foo-bar.fish
                     eval "$(env _PYWBEMLISTENER_COMPLETE=
                           fish_source pywbemlistener)"
=====  ===========  ===========================================================

To activate pywbemlistener tab-completion:

  1. Edit the eval command in the startup file or
  2. Close the file and restart the terminal or
  3. Test existence of tab-completion by:
     a. Test completion with a command such as "pywbemlistener cl<TAB> which
        should complete the "pywbemlistener li<TAB>" command group name.
     b. In bash executing "complete -p pywbemlistener". An entry for
        pywbemlistener must exist for pywbemlistener as follows:
        complete -o nosort -F _pywbemlistener_completion pywbemlistener

Executing the eval directly in the shell startup file has the issue that the
pywbemlistener executable location must be known when opening a terminal . This
may not be consistent with executing pywbemlistener in virtual environments.

To activate tab-completion using a completion file execute the command defined
below for the desired shell. This  creates the completion script for
pywbemlistener in ``~/pywbemlistener-complete.bash``. This command requires
that pywbemlistener is publicly available :

=====  =====================================================================
shell  completion file creating command
=====  =====================================================================
bash   _PYWBEMLISTENER_COMPLETE=bash_source pywbemlistener >
            ~/.pywbemcli-complete.bash
zsh    _PYWBEMLISTENER_COMPLETE=zsh_source pywbemlistener >
            ~/.pywbemcli-complete.zsh
fish   _PYWBEMLISTENER_COMPLETE=fish_source pywbemlistener >
          ~/.config/fish/completions/pywbemcli.fish
=====  =====================================================================

Once the completion script file is created, pywbemlistener tab-completion can
be activated by sourcing this script:
   (ex. ''source ~/.pywbemlistener-complete.bash'').
This does not call pywbemlistener and can be done by, for for example:

* Include the sourcing statement in the shell startup script (ex. ~/.bashrc)
* Execute the statement as part of the startup of virtual envrionments.
* Manually executing the sourcing statement when required.
'''
# pylint: enable=invalid-name


# pylint: disable=invalid-name
tab_completion_help_msg = """
Tab completion (when activated) for option values and arguments exists when the
data is local. It is not provided for option values and arguments where access
to a WBEM server is required.

Tab completion is available for at least the following parts of the command
line:

* The executable name
* The command names (ex. list)
* The option names (names starting with '-' or '--')
* The values of some general options including:
    * --keyfile
    * --certfile
    * --output_format
* The values of some arguements
    * pywbemlistener help <subject> argument
    * lywbemlistener show, delete <name> argument

When tab completion is not available for an argument or option value, entering
<TAB> does nothing.
"""


###########################################################################
#
#  Table of subjects
#
###########################################################################

PYWBEMLISTENER_HELP_SUBJECTS_DICT = {
    'activate': ("Activating shell tab completion",
                 activate_shell_help_msg),
    'tab-completion': ("Where tab completion is provided by pywbemlistener",
                       tab_completion_help_msg)
}
