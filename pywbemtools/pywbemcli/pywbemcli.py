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
import sys
import traceback
import click
import click_repl
from prompt_toolkit.history import FileHistory

import pywbem

from ._context_obj import ContextObj
from ._common import GENERAL_OPTIONS_METAVAR, TABLE_FORMATS, \
    CIM_OBJECT_OUTPUT_FORMATS, warning_msg
from ._pywbem_server import PywbemServer
from .config import DEFAULT_OUTPUT_FORMAT, DEFAULT_NAMESPACE, \
    PYWBEMCLI_PROMPT, PYWBEMCLI_HISTORY_FILE, DEFAULT_MAXPULLCNT, \
    DEFAULT_CONNECTION_TIMEOUT, MAX_TIMEOUT

from ._connection_repository import ConnectionRepository, \
    DEFAULT_CONNECTIONS_FILE

__all__ = ['cli']

PYWBEM_VERSION = "pywbem, version {}".format(pywbem.__version__)

# Defaults for some options
DEFAULT_TIMESTATS = False
DEFAULT_PULL_CHOICE = 'either'
USE_PULL_CHOICE = {'either': None, 'yes': True, 'no': False}

# enable -h as additional help option
CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


# pylint: disable=bad-continuation
@click.group(invoke_without_command=True,
             context_settings=CONTEXT_SETTINGS,
             options_metavar=GENERAL_OPTIONS_METAVAR)
@click.option('-s', '--server', type=str, envvar=PywbemServer.server_envvar,
              metavar='URI',
              help='Hostname or IP address with scheme of the WBEM server in '
                   'format:\n[{scheme}://]{host}[:{port}]\n'
                   '* Scheme: must be "https" or "http" [Default: "https"]\n'
                   '* Host: defines short/fully qualified DNS hostname, '
                   'literal IPV4 address (dotted), or literal IPV6 address\n'
                   '* Port: (optional) defines WBEM server port to be '
                   'used [Defaults: 5988(HTTP) and 5989(HTTPS)].\n'
                   'This option, the --name, and --mock-server are '
                   'mututally exclusive since each defines a WBEM server.\n' +
                   '(EnvVar: {ev})'.format(ev=PywbemServer.server_envvar))
@click.option('-n', '--name', type=str,
              metavar='NAME',
              envvar=PywbemServer.name_envvar,
              help='Name for the connection.  If this '
                   'option exists and the server option does not exist '
                   'pywbemcli retrieves the connection information from the '
                   'connections file ' +
                   '({cf}). '.format(cf=DEFAULT_CONNECTIONS_FILE) +
                   'This option, --server, and --mock-server are mutually '
                   'exclusive since each defines a WBEM server.\n' +
                   '(EnvVar: {ev})'.format(ev=PywbemServer.name_envvar))
@click.option('-d', '--default-namespace', type=str,
              metavar='NAMESPACE',
              envvar=PywbemServer.defaultnamespace_envvar,
              help='Default namespace to use in the target WBEM server if no '
                   'namespace is defined in a subcommand.\n' +
                   '(EnvVar: {ev})\n' .format(ev=PywbemServer.name_envvar) +
                   '[Default: {of}]'.format(of=DEFAULT_NAMESPACE))
@click.option('-u', '--user', type=str, envvar=PywbemServer.user_envvar,
              metavar='USER',
              help='User name for the WBEM server connection.\n' +
                   '(EnvVar: {ev})' .format(ev=PywbemServer.user_envvar))
@click.option('-p', '--password', type=str,
              metavar='PASSWORD',
              envvar=PywbemServer.password_envvar,
              help='Password for the WBEM server. Will be requested as part '
                   ' of initialization if user name exists and it is not '
                   ' provided by this option.\n' +
                   '(EnvVar: {ev})'.format(ev=PywbemServer.password_envvar))
@click.option('-t', '--timeout', type=click.IntRange(0, MAX_TIMEOUT),
              metavar='INTEGER',
              envvar=PywbemServer.timeout_envvar,
              help='Client timeout completion of WBEM server operation in '
                   'seconds.\n' +
                   '(EnvVar: {ev})'.format(ev=PywbemServer.timeout_envvar))
@click.option('-N', '--no-verify', is_flag=True,
              envvar=PywbemServer.no_verify_envvar,
              help='If set, client does not verify WBEM server certificate.' +
                   '(EnvVar: {ev}).'.format(ev=PywbemServer.no_verify_envvar))
@click.option('-c', '--certfile', type=str,
              envvar=PywbemServer.certfile_envvar,
              help="Server certfile. Ignored if --no-verify flag set. " +
                   '(EnvVar: {ev}).'.format(ev=PywbemServer.certfile_envvar))
@click.option('-k', '--keyfile', type=str,
              metavar='FILE PATH',
              envvar=PywbemServer.keyfile_envvar,
              help='Client private key file.\n'
                   '(EnvVar: {ev})'.format(ev=PywbemServer.keyfile_envvar))
@click.option('--ca-certs', type=str,
              envvar=PywbemServer.ca_certs_envvar,
              help='File or directory containing certificates that will be '
                   'matched against certificate received from WBEM '
                   'server. Set --no-verify option to bypass '
                   'client verification of the WBEM server certificate.\n'
                   '(EnvVar: {ev})\n'.format(ev=PywbemServer.ca_certs_envvar) +
                   '[Default: Searches for matching certificates in the '
                   'following system directories:\n' +
                   ',\n'.join(pywbem.DEFAULT_CA_CERT_PATHS) + ']')
@click.option('-o', '--output-format',
              metavar='<choice>',
              envvar=PywbemServer.timeout_envvar,
              help='Choice for command output data format. '
                   'pywbemcli may override the format choice depending on the '
                   'command group and command since not all formats apply to '
                   'all output data types. Choices further defined in '
                   'pywbemcli documentation.\n' +
                   'Choices: Table: [{tb}], Object: [{ob}]\n'
                   .format(tb='|'.join(TABLE_FORMATS),
                           ob='|'.join(CIM_OBJECT_OUTPUT_FORMATS)) +
                   '[Default: "{}"]'.format(DEFAULT_OUTPUT_FORMAT))
@click.option('-U', '--use-pull',
              envvar=PywbemServer.use_pull_envvar,
              type=click.Choice(['yes', 'no', 'either']),
              help='Determines whether pull operations are used for '
                   'EnumerateInstances, AssociatorInstances, '
                   'ReferenceInstances, and ExecQuery operations.\n'
                   '* "yes": pull operations required; if server '
                   'does not support pull, the operation fails.\n'
                   '* "no": forces pywbemcli to use only the '
                   'traditional non-pull operations.\n'
                   '* "either": pywbemcli trys first pull and then '
                   'traditional operations.\n' +
                   '(EnvVar: {ev}) '.format(ev=PywbemServer.use_pull_envvar) +
                   '[Default: {}]'.format(DEFAULT_PULL_CHOICE))
@click.option('--pull-max-cnt', type=int,
              help='Maximium object count of objects to be returned for '
                   'each request if pull operations are used. Must be  a '
                   'positive non-zero integer.\n' +
                   '(EnvVar: {ev})\n'.
                   format(ev=PywbemServer.pull_max_cnt_envvar) +
                   '[Default: {}]'.format(DEFAULT_MAXPULLCNT))
@click.option('-T', '--timestats', is_flag=True,
              help='Show time statistics of WBEM server operations after '
                   'each command execution.')
@ click.option('-l', '--log', type=str,
               metavar='COMP=DEST:DETAIL,...',
               envvar=PywbemServer.log_envvar,
               help='Enable logging of CIM Operations and set a COMPONENT to '
                    'a log level, DESTINATION, and DETAIL level.\n'
                    '* COMP: [{c}], Default: {cd}\n'
                    '* DEST: [{d}], Default: {dd}\n'
                    '* DETAIL:[{dl}], Default: {dll}'
                    .format(c='|'.join(pywbem.LOGGER_SIMPLE_NAMES),
                            cd='all',
                            d='|'.join(pywbem.LOG_DESTINATIONS),
                            dd=pywbem.DEFAULT_LOG_DESTINATION,
                            dl='|'.join(pywbem.LOG_DETAIL_LEVELS),
                            dll=pywbem.DEFAULT_LOG_DETAIL_LEVEL))
@click.option('-v', '--verbose', is_flag=True,
              help='Display extra information about the processing.')
@click.option('-m', '--mock-server', type=str, multiple=True,
              envvar=PywbemServer.mock_server_envvar,
              metavar="FILENAME",
              help='Defines, a mock WBEM server as the target WBEM server. '
                   'The option value defines a MOF or Python file path used to '
                   'populate the mock repository. This option may be used '
                   'multiple times where each use defines a single file_path.'
                   'This option, --server, and --name '
                   'are mutually exclusive since each defines a WBEM server. '
                   'See the pywbemtools documentation for more '
                   'information.\n' +
                   "(EnvVar: {ev})".
                   format(ev=PywbemServer.mock_server_envvar))
@click.version_option(
    message='%(prog)s, version %(version)s\n' + PYWBEM_VERSION,
    help='Show the version of this command and the pywbem package and exit.')
@click.pass_context
def cli(ctx, server, name, default_namespace, user, password, timeout,
        no_verify, certfile, keyfile, ca_certs, output_format, use_pull,
        pull_max_cnt, verbose, mock_server, pywbem_server=None, timestats=None,
        log=None):
    """
    Pywbemcli is a command line WBEM client that uses the DMTF CIM-XML protocol
    to communicate with WBEM servers. Pywbemcli can:

    \b
    * Manage the information in WBEM servers CIM objects using the
      operations defined in the DMTF specification.  It can manage CIM
      classes, CIM instances and CIM qualifier declarations in the WBEM
      Server and execute CIM methods and queries on the server.

    \b
    * Inspect WBEM server characteristics including namespaces, registered
      profiles, and other server information.

    \b
    * Capture detailed information on communication with the WBEM
      server including time statistics and logs of the operations.

    \b
    * Maintain a persistent list of named connections to WBEM servers
      and execute operations on them by name.

    Pywbemcli implements command groups and subcommands to execute the CIM-XML
    operations defined by the DMTF CIM Operations Over HTTP specification
    (DSP0200).

    The general options shown below can also be specified on any of the
    (sub)commands as well as the command line.

    For more detailed documentation, see:

        https://pywbemtools.readthedocs.io/en/stable/
    """
    # In interactive mode, general options specified in cmd line are used as
    # defaults for interactive commands.
    # This requires being able to determine for each option whether it has been
    # specified and is why general options don't define defaults in the
    # decorators that define them.
    if ctx.obj is None:
        # In command mode or processing the command line options in
        # interactive mode. Apply the documented option defaults.
        # Default for output_format is applied in processing since it depends
        # on request (ex. mof for get class vs table for many)

        resolved_default_namespace = default_namespace or DEFAULT_NAMESPACE

        resolved_timestats = timestats or DEFAULT_TIMESTATS

        if server and name:
            click.echo('The --name option "%s" and --server option "%s" '
                       'are mutually exclusive and may not be used '
                       'simultaneously' % (name, server), err=True)
            raise click.Abort()

        # process mock_server option
        resolved_mock_server = []
        if mock_server:
            assert isinstance(mock_server, tuple)
            resolved_mock_server = []
            # resolve relative and absolute paths
            mock_server_path = []
            for fn in mock_server:
                if fn == os.path.basename(fn):
                    mock_server_path.append(os.path.join(os.getcwd(), fn))
                else:
                    mock_server_path.append(fn)

            # Abort for non-existent mock files or invalid type
            # Otherwise these issued do not get found until connection
            # exercised.
            # TODO: Future: Create common method with code in build_respository
            for file_path in mock_server_path:
                ext = os.path.splitext(file_path)[1]
                if ext not in ['.py', '.mof']:
                    click.echo('Error: --mock-server: File: "%s" '
                               'extension: "%s" not valid. "py" or "mof" '
                               'required' % (file_path, ext), err=True)
                    raise click.Abort()
                if not os.path.isfile(file_path):
                    click.echo('Error: --mock-server: File: "%s" does '
                               'not exist' % file_path, err=True)
                    raise click.Abort()
                if ext != '.py':
                    resolved_mock_server.append(file_path)
                    continue

                with open(file_path) as fp:
                    if '!PROCESS!AT!STARTUP!' in fp.readline():
                        try:
                            # Only verbose is allowed here
                            globalparams = {'VERBOSE': verbose}
                            # pylint: disable=exec-used
                            exec(fp.read(), globalparams, None)
                        except Exception as ex:
                            exc_type, exc_value, exc_traceback = \
                                sys.exc_info()
                            tb = repr(traceback.format_exception(
                                exc_type,
                                exc_value,
                                exc_traceback))
                            raise click.ClickException('Exception failure of '
                                                       '"--mock-server" python '
                                                       'script %r. '
                                                       'Exception: %r\n'
                                                       'Traceback\n%s' %
                                                       (file_path, ex, tb))
                    else:  # not processed during startup
                        resolved_mock_server.append(file_path)

        # The mock-server that leaves something in resolved server
        # and name simultaneously fail.
        if server and resolved_mock_server:
            click.echo('Error: Conflicting server definitions. Do not use '
                       '--server and --mock-server simultaneously. '
                       '--server: %s, --mock-server: %s' %
                       (server, resolved_mock_server), err=True)
            raise click.Abort()

        if resolved_mock_server and name:
            click.echo('The --name "%s" option and --server "%s" option '
                       'are mutually exclusive and may not be used '
                       'simultaneously' % (name, mock_server), err=True)
            raise click.Abort()

        if use_pull:
            try:
                resolved_use_pull = USE_PULL_CHOICE[use_pull]
            except KeyError:
                raise click.ClickException(
                    'Invalid choice for --use_pull %s' % use_pull)
        else:
            resolved_use_pull = DEFAULT_PULL_CHOICE

        resolved_pull_max_cnt = pull_max_cnt or DEFAULT_MAXPULLCNT

        resolved_timeout = timeout or DEFAULT_CONNECTION_TIMEOUT

        # Create the PywbemServer object (this contains all of the info
        # for the connection defined by the cmd line input)
        if server or mock_server:
            if name:
                click.echo("Name found with server or mock-server", err=True)
                click.Abort()
            name = 'default'
            pywbem_server = PywbemServer(server,
                                         resolved_default_namespace,
                                         name=name,
                                         user=user,
                                         password=password,
                                         timeout=resolved_timeout,
                                         no_verify=no_verify,
                                         certfile=certfile,
                                         keyfile=keyfile,
                                         ca_certs=ca_certs,
                                         use_pull=resolved_use_pull,
                                         pull_max_cnt=resolved_pull_max_cnt,
                                         stats_enabled=resolved_timestats,
                                         verbose=verbose,
                                         mock_server=resolved_mock_server,
                                         log=log)
        else:  # Server and mock_server are None
            # if name cmd line option, get connection repo and
            # get name from the repo.
            pywbemcli_servers = ConnectionRepository()
            s_name = None
            if name:
                if name in pywbemcli_servers:
                    s_name = name
                # exception when defined name does not exist
                else:
                    raise click.ClickException('Named connection "{}" does '
                                               'not exist and no --server or '
                                               '--mock-server options to '
                                               'define a '
                                               'WBEM server'.format(name))
            else:
                # try default but ignore if it does not exist
                if 'default' in pywbemcli_servers:
                    s_name = name

            # Get the named connection from the repo
            if s_name:
                pywbem_server = pywbemcli_servers[name]
                # Test for invalid other options with the --name option
                # The following options are part of each PywbemServer object
                # TODO: FUTURE should really put this into pywbemserver itself.
                other_options = ((default_namespace, 'default_namespace'),
                                 (use_pull, 'use_pull'),
                                 (pull_max_cnt, ''),
                                 (timeout, 'timeout'),
                                 (no_verify, 'no_verify'),
                                 (user, 'user'),
                                 (certfile, 'certfile'),
                                 (keyfile, 'keyfile'),
                                 (ca_certs, 'ca_certs'),
                                 (server, 'server'),
                                 (mock_server, 'mock-server'))

                for option in other_options:
                    if option[0]:
                        warning_msg('"%s %s" ignored when "-n/--name '
                                    'used' % (option[1], option[0]))
                # NOTE: The log definition is only for this session.
                if log:
                    # pylint: disable=protected-access
                    pywbem_server._log = log

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
        if use_pull is None:
            resolved_use_pull = ctx.obj.use_pull
        if pull_max_cnt is None:
            resolved_pull_max_cnt = ctx.obj.use_pull
        if not timestats:  # Defaults to False, not None
            resolved_timestats = ctx.obj.timestats
        if log is None:
            log = ctx.obj.log
        if verbose is None:
            verbose = ctx.obj.verbose
    # Create a command context for each command: An interactive command has
    # its own command context different from the command context for the
    # command line.

    ctx.obj = ContextObj(pywbem_server, output_format,
                         resolved_use_pull,
                         resolved_pull_max_cnt,
                         resolved_timestats,
                         log, verbose)

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
    Enter interactive mode (default).

    Enters the interactive mode where subcommands can be entered interactively
    and load the command history file.

    If no options are specified on the command line, the interactive mode
    is entered. The prompt is changed to 'pywbemcli>' in the interactive
    mode.

    Pywbemcli may be terminated from this mode by entering
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
