# (C) Copyright 2021 Inova Development Inc.
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
The main function of the pywbemlistener command.
"""

import warnings
import click

from pywbem import __version__ as pywbem_version

from ._context_obj import ContextObj
from . import _config
from .._click_extensions import PywbemtoolsTopGroup, GENERAL_OPTS_TXT, \
    SUBCMD_HELP_TXT
from .._utils import get_terminal_width
from .._options import add_options, help_option
from .._output_formatting import OUTPUT_FORMAT_GROUPS, OUTPUT_FORMATS

__all__ = ['cli']


#
# Context variables passed to click
#

CONTEXT_SETTINGS = {

    # Enable -h as additional help option:
    "help_option_names": ['-h', '--help'],

    # Default the output width properly:
    "terminal_width": get_terminal_width()}


############################################################################
#
#   cli command (main entry point) and definition of all of the pywbemlistener
#   general options.
#
############################################################################


# pylint: disable=bad-continuation
# PywbemtoolsTopGroup sets order commands listed in help output
@click.group(invoke_without_command=False, cls=PywbemtoolsTopGroup,
             context_settings=CONTEXT_SETTINGS,
             options_metavar=GENERAL_OPTS_TXT,
             subcommand_metavar=SUBCMD_HELP_TXT,
             move_to_end=['run', 'docs'])
@click.option('-o', '--output-format', metavar='FORMAT',
              type=click.Choice(OUTPUT_FORMATS),
              default=None,
              help='Output format for the command result. '
                   'FORMAT is one of the table formats: [{tb}].'.
                   format(tb='|'.join(OUTPUT_FORMAT_GROUPS['TABLE'][0])))
@click.option('-l', '--logdir',
              type=click.Path(exists=False, dir_okay=True),
              metavar='DIR',
              default=None,
              envvar=_config.PYWBEMLISTENER_LOGDIR_ENVVAR,
              help="Enable logging of the 'pywbemlistener run' command output "
                   "to a file in a log directory. The file will be named "
                   "'pywbemlistener_NAME.log' where NAME is the listener "
                   "name. Default: EnvVar {ev}, or no logging.".
                   format(ev=_config.PYWBEMLISTENER_LOGDIR_ENVVAR))
@click.option('-v', '--verbose', count=True,
              help='Verbosity level. Can be specified multiple times: '
                   '-v: {}; -vv: {}.'.
              format(_config.VERBOSE_1_HELP, _config.VERBOSE_2_HELP))
@click.option('--pdb', is_flag=True,
              default=False,
              envvar=_config.PYWBEMLISTENER_PDB_ENVVAR,
              help='Pause execution in the built-in pdb debugger just before '
                   'executing the command within pywbemlistener. '
                   'Default: EnvVar {ev}, or no debugger.'.
                   format(ev=_config.PYWBEMLISTENER_PDB_ENVVAR))
@click.option('--warn', is_flag=True,
              default=False,
              help='Enable display of all Python warnings. '
                   'Default: Leave warning control to the PYTHONWARNINGS '
                   'EnvVar, which by default displays no warnings.')
@click.version_option(
    message='%(prog)s, version %(version)s\npywbem, version {}'.format(
        pywbem_version),
    help='Show the version of this command and the pywbem package.')
@add_options(help_option)
@click.pass_context
def cli(ctx, output_format, logdir, verbose, pdb, warn):
    """
    The pywbemlistener command can run and manage WBEM listeners.

    Each listener is a process that executes the 'pywbemlistener run'
    command to receive WBEM indications sent from a WBEM server.

    A listener process can be started with the 'pywbemlistener start'
    command and stopped with the 'pywbemlistener stop' command.

    There is no central registration of the currently running listeners.
    Instead, the currently running processes executing the
    'pywbemlistener run' command are by definition the currently running
    listeners. Because of this, there is no notion of a stopped listener nor
    does a listener have an operational status.

    The general options shown below can also be specified on any of the
    commands, positioned right after the 'pywbemlistener' command name.

    The width of help texts of this command can be set with the
    PYWBEMTOOLS_TERMWIDTH environment variable.

    For more detailed documentation, see:

        https://pywbemtools.readthedocs.io/en/stable/
    """

    if warn:
        warnings.simplefilter('once')
    # else: Leave warning control to the PYTHONWARNINGS env var.

    if verbose >= _config.VERBOSE_PROCESSES:
        _config.VERBOSE_PROCESSES_ENABLED = True

    # Since there is no interactive mode, there is never a context object.
    assert ctx.obj is None
    ctx.obj = ContextObj(output_format, logdir, verbose, pdb, warn)
