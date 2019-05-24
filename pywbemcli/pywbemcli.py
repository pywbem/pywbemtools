# (C) Copyright 2017 IBM Corp.
# (C) Copyright 2017 Inova Development Inc.
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
Click command definition for the pywbemcli command, the top level command for
the pywbemcli click tool
"""
from __future__ import absolute_import

import os
import click_repl
import click
from prompt_toolkit.history import FileHistory

from pywbem import DEFAULT_CA_CERT_PATHS, LOGGER_SIMPLE_NAMES, \
    LOG_DESTINATIONS, DEFAULT_LOG_DESTINATION, LOG_DETAIL_LEVELS, \
    DEFAULT_LOG_DETAIL_LEVEL

from ._context_obj import ContextObj
from ._common import GENERAL_OPTIONS_METAVAR, TABLE_FORMATS, \
    CIM_OBJECT_OUTPUT_FORMATS
from ._pywbem_server import PywbemServer
from .config import DEFAULT_OUTPUT_FORMAT, DEFAULT_NAMESPACE, \
    PYWBEMCLI_PROMPT, PYWBEMCLI_HISTORY_FILE, DEFAULT_MAXPULLCNT, \
    DEFAULT_CONNECTION_TIMEOUT, MAX_TIMEOUT

from ._connection_repository import ConnectionRepository


__all__ = ['cli']

# Defaults for some options
DEFAULT_TIMESTATS = False
DEFAULT_PULL_CHOICE = 'either'
# enable -h as additional help option
CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


# pylint: disable=bad-continuation
@click.group(invoke_without_command=True,
             context_settings=CONTEXT_SETTINGS,
             options_metavar=GENERAL_OPTIONS_METAVAR)
@click.option('-s', '--server', type=str, envvar=PywbemServer.server_envvar,
              metavar='URI',
              help='Hostname or IP address with scheme of the WBEMServer in '
                   'format:\n[{scheme}://]{host}[:{port}]\n'
                   'The server parameter is conditionally optional '
                   '(see --name)\n'
                   '* Scheme: must be "https" or "http" [Default: "https"]\n'
                   '* Host: defines short/fully qualified DNS hostname, '
                   'literal IPV4 address (dotted), or literal IPV6 address\n'
                   '* Port: (optional) defines WBEM server port to be '
                   'used '
                   '[Defaults: 5988(HTTP) and 5989(HTTPS)].\n' +
                   '(EnvVar: {ev}).'.format(ev=PywbemServer.server_envvar))
@click.option('-N', '--name', type=str,
              metavar='NAME',
              envvar=PywbemServer.name_envvar,
              help='Name for the connection(optional, see --server).  If this '
                   'option exists and the server option does not exist '
                   'pywbemcli attempts to retrieve the connection information '
                   'from the connections file. If the server option exists '
                   'that is used as the connection definition with the name '
                   '"default". '
                   'This option and --server are mutually exclusive.' +
                   '(EnvVar: {ev}).'.format(ev=PywbemServer.name_envvar))
@click.option('-d', '--default_namespace', type=str,
              metavar='NAMESPACE',
              envvar=PywbemServer.defaultnamespace_envvar,
              help='Default Namespace to use in the target WBEMServer if no '
                   'namespace is defined in the subcommand' +
                   '(EnvVar: {ev}) ' .format(ev=PywbemServer.name_envvar) +
                   '[]Default: {of}].'.format(of=DEFAULT_NAMESPACE))
@click.option('-u', '--user', type=str, envvar=PywbemServer.user_envvar,
              metavar='USER',
              help='User name for the WBEM Server connection. ' +
                   '(EnvVar: {ev}) ' .format(ev=PywbemServer.name_envvar))
@click.option('-p', '--password', type=str,
              metavar='PASSWORD',
              envvar=PywbemServer.password_envvar,
              help='Password for the WBEM Server. Will be requested as part '
                   ' of initialization if user name exists and it is not '
                   ' provided by this option.' +
                   '(EnvVar: {ev}).'.format(ev=PywbemServer.password_envvar))
@click.option('-t', '--timeout', type=click.IntRange(0, MAX_TIMEOUT),
              metavar='INTEGER',
              envvar=PywbemServer.timeout_envvar,
              help="Operation timeout for the WBEM Server in seconds.\n"
                   '(EnvVar: PYWBEMCLI_{})'.format(PywbemServer.timeout_envvar))
@click.option('-n', '--noverify', is_flag=True,
              envvar=PywbemServer.noverify_envvar,
              help='If set, client does not verify server certificate.' +
                   '(EnvVar: {ev}).'.format(ev=PywbemServer.noverify_envvar))
@click.option('-c', '--certfile', type=str,
              envvar=PywbemServer.certfile_envvar,
              help="Server certfile. Ignored if noverify flag set. " +
                   '(EnvVar: {ev}).'.format(ev=PywbemServer.certfile_envvar))
@click.option('-k', '--keyfile', type=str,
              metavar='FILE PATH',
              envvar=PywbemServer.keyfile_envvar,
              help='Client private key file. '
                   '(EnvVar: {}).'.format(PywbemServer.keyfile_envvar))
@click.option('--ca_certs', type=str,
              envvar=PywbemServer.ca_certs_envvar,
              help='File or directory containing certificates that will be '
                   'matched against certificate received from WBEM '
                   'server. Set --no-verify-cert option to bypass '
                   'client verification of the WBEM server certificate. '
                   ' (EnvVar: PYWBEMCLI_CA_CERTS).\n'
                   '[Default: Searches for matching certificates in the '
                   'following system directories:'
                   ' ' + ("\n".join("%s]" % p for p in DEFAULT_CA_CERT_PATHS)))
@click.option('-o', '--output-format',
              metavar='<choice>',
              envvar=PywbemServer.timeout_envvar,
              help='Output format. Multiple table and CIMObjects formats. '
                   'pywbemcli may override the format choice depending on the '
                   'operation since not all formats apply to all output data '
                   'types. Choices further defined in documentation.\n' +
                   'Choices: Table: [{tb}], Object: [{ob}]\n'
                   .format(tb='|'.join(TABLE_FORMATS),
                           ob='|'.join(CIM_OBJECT_OUTPUT_FORMATS)) +
                   '[Default: "{}"]'.format(DEFAULT_OUTPUT_FORMAT))
@click.option('--use-pull_ops',
              envvar=PywbemServer.use_pull_envvar,
              type=click.Choice(['yes', 'no', 'either']),
              help='Determines whether the pull operations are used for '
                   'EnumerateInstances, associatorinstances, '
                   'referenceinstances, and ExecQuery operations.\n'
                   '* "yes": pull operations used; if server '
                   'does not support pull, the operation will fail.\n'
                   '* "no": forces pywbemcli to try only the '
                   'traditional non-pull operations.\n'
                   '* "either": pywbemcli trys first pull and then '
                   ' traditional operations.\n' +
                   '(EnvVar: {}) '.format(PywbemServer.use_pull_envvar) +
                   '[Default: {}]'.format(DEFAULT_PULL_CHOICE))
@click.option('--pull-max-cnt', type=int,
              help='MaxObjectCount of objects to be returned for each request '
                   'if pull operations are used. Must be  a positive non-zero '
                   'integer.' +
                   '(EnvVar: {}) '.format(PywbemServer.pull_max_cnt_envvar) +
                   '[Default: {}]'.format(DEFAULT_MAXPULLCNT))
@click.option('-T', '--timestats', is_flag=True,
              help='Show time statistics of WBEM server operations after '
                   'each command execution.')
@ click.option('-l', '--log', type=str,
               metavar='COMP=DEST:DETAIL,...',
               envvar=PywbemServer.log_envvar,
               help='Enable logging of CIM Operations and set a component to '
                    'a log level, destination, and detail level.\n'
                    '* COMP: [{c}], Default: {cd}\n'
                    '* DEST: [{d}], Default: {dd}\n'
                    '* DETAIL:[{dl}], Default: {dll}'
                    .format(c='|'.join(LOGGER_SIMPLE_NAMES),
                            cd='all',
                            d='|'.join(LOG_DESTINATIONS),
                            dd=DEFAULT_LOG_DESTINATION,
                            dl='|'.join(LOG_DETAIL_LEVELS),
                            dll=DEFAULT_LOG_DETAIL_LEVEL))
@click.option('-v', '--verbose', is_flag=True,
              help='Display extra information about the processing.')
@click.option('-m', '--mock-server', type=str, multiple=True,
              envvar=PywbemServer.mock_server_envvar,
              metavar="FILENAME",
              help='Defines, a mock WBEM server is as the target WBEM server. '
                   'The option value defines a MOF or Python file path used to '
                   'populate the mock repository. This option may be used '
                   'multiple times where each use defines a single file_path.'
                   'See the pywbemtools documentation for more information.' +
                   "(EnvVar: {}).".format(PywbemServer.mock_server_envvar))
@click.version_option(help='Show the version of this command and the package '
                      'and exit')
@click.pass_context
def cli(ctx, server, name, default_namespace, user, password, timeout, noverify,
        certfile, keyfile, ca_certs, output_format, use_pull_ops, pull_max_cnt,
        verbose, mock_server, pywbem_server=None, timestats=None, log=None):
    """
    WBEM Server command line browser. This cli tool implements the
    CIM/XML client APIs as defined in pywbem to make requests to a WBEM
    server. This browser uses subcommands to:

    \b
        * Explore the characteristics of WBEM Servers based on using the
          pywbem client APIs.  It can manage/inspect CIM_Classes and
          CIM_instances on the server.

    \b
        * In addition it can inspect namespaces, profiles, subscriptions,
          and other server information and inspect and manage WBEM
          indication subscriptions.

    The global options shown above that can also be specified on any of the
    (sub-)commands as well as the command line.
    """

    # In interactive mode, global options specified in cmd line are used as
    # defaults for interactive commands.
    # This requires being able to determine for each option whether it has been
    # specified and is why global options don't define defaults in the
    # decorators that define them.

    if ctx.obj is None:
        # In command mode or processing the command line options in
        # interactive mode. Apply the documented option defaults.
        # Default for output_format is applied in processing since it depends
        # on request (ex. mof for get class vs table for many)
        if default_namespace is None:
            default_namespace = DEFAULT_NAMESPACE

        if timestats is None:
            timestats = DEFAULT_TIMESTATS

        if mock_server:
            assert isinstance(mock_server, tuple)
            new_mock_server = []
            # allow relative or absolute paths
            for fn in mock_server:
                if fn == os.path.basename(fn):
                    new_mock_server.append(os.path.join(os.getcwd(), fn))
                else:
                    new_mock_server.append(fn)
            mock_server = new_mock_server

        if use_pull_ops:
            if use_pull_ops == 'either':
                use_pull_ops = None
            elif use_pull_ops == 'yes':
                use_pull_ops = True
            elif use_pull_ops == 'no':
                use_pull_ops = False
            else:
                raise click.ClickException(
                    'Invalid choice for use_pull_ops %s' % use_pull_ops)
        else:
            use_pull_ops = 'either'
        if pull_max_cnt is None:
            pull_max_cnt = DEFAULT_MAXPULLCNT
        if timeout is None:
            timeout = DEFAULT_CONNECTION_TIMEOUT

        # Create the PywbemServer object (this contains all of the info
        # for the connection defined by the cmd line input)
        if server or mock_server:
            if not name:
                name = 'default'
            pywbem_server = PywbemServer(server,
                                         default_namespace,
                                         name=name,
                                         user=user,
                                         password=password,
                                         timeout=timeout,
                                         noverify=noverify,
                                         certfile=certfile,
                                         keyfile=keyfile,
                                         ca_certs=ca_certs,
                                         use_pull_ops=use_pull_ops,
                                         pull_max_cnt=pull_max_cnt,
                                         stats_enabled=timestats,
                                         verbose=verbose,
                                         mock_server=mock_server,
                                         log=log)
        else:  # no server and mock_server are None
            # if name cmd line option, get connection repo and
            # search for name
            if name:
                pywbemcli_servers = ConnectionRepository()
                if name in pywbemcli_servers:
                    pywbem_server = pywbemcli_servers[name]
                    # NOTE: The log definition is only for this session.
                    if log:
                        # pylint: disable=protected-access
                        pywbem_server._log = log
                else:
                    raise click.ClickException('%s named connection does not '
                                               'exist' % name)
            else:
                pywbemcli_servers = ConnectionRepository()
                if 'default' in pywbemcli_servers:
                    pywbem_server = pywbemcli_servers['default']
                else:
                    # If no server defined, set None. This allows subcmds that
                    # donot require a server executed without the server
                    # defined.
                    pywbem_server = None

    else:  # ctx.obj exists. Processing an interactive command.
        # Apply the option defaults from the command line options.
        if pywbem_server is None:
            pywbem_server = ctx.obj.pywbem_server
        if output_format is None:
            output_format = ctx.obj.output_format
        if use_pull_ops is None:
            output_format = ctx.obj.use_pull_ops
        if pull_max_cnt is None:
            output_format = ctx.obj.use_pull_ops
        if pywbem_server is None:
            timestats = ctx.obj.pull_max_cnt
        if log is None:
            log = ctx.obj.log
        if verbose is None:
            verbose = ctx.obj.verbose
    # Create a command context for each command: An interactive command has
    # its own command context different from the command context for the
    # command line.

    ctx.obj = ContextObj(pywbem_server, output_format, use_pull_ops,
                         pull_max_cnt, timestats, log, verbose)

    # Invoke default command
    if ctx.invoked_subcommand is None:
        ctx.invoke(repl)


@cli.command('help')
@click.pass_context
def repl_help(ctx):  # pylint: disable=unused-argument
    """
    Show help message for interactive mode.
    """
    print("""
The following can be entered in interactive mode:

  <pywbemcli-cmd>             Execute pywbemcli command <pywbemcli-cmd>.
  !<shell-cmd>                Execute shell command <shell-cmd>.

  <CTRL-D>, :q, :quit, :exit  Exit interactive mode.

  <TAB>                       Tab completion (can be used anywhere).
  -h, --help                  Show pywbemcli general help message, including a
                              list of pywbemcli commands.
  <pywbemcli-cmd> --help      Show help message for pywbemcli command
                              <pywbemcli-cmd>.
  help                        Show this help message.
  :?, :h, :help               Show help message about interactive mode.
  <up-arrow, down-arrow>      View pwbemcli command history:
""")


@cli.command('repl')
@click.pass_context
def repl(ctx):
    """
    Enter interactive (REPL) mode (default).

    Enters the interactive mode where subcommands can be entered interactively
    and load the command history file.

    If no options are specified on the command line,  the interactive mode
    is entered. The prompt is changed to `pywbemcli>' in the interactive
    mode.

    Pywbemcli may be terminated form this mode by entering
    <CTRL-D>, :q, :quit, :exit

    Parameters:

      ctx (:class:`click.Context`): The click context object. Created by the
        ``@click.pass_context`` decorator.
    """

    history_file = PYWBEMCLI_HISTORY_FILE
    if history_file.startswith('~'):
        history_file = os.path.expanduser(history_file)

    print("Enter 'help' for help, <CTRL-D> or ':q' to exit pywbemcli.")

    prompt_kwargs = {
        'message': PYWBEMCLI_PROMPT,
        'history': FileHistory(history_file),
    }
    click_repl.repl(ctx, prompt_kwargs=prompt_kwargs)
