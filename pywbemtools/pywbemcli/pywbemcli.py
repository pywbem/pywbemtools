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
from pywbem import DEFAULT_CA_CERT_PATHS, LOGGER_SIMPLE_NAMES, \
    LOG_DESTINATIONS, DEFAULT_LOG_DESTINATION, LOG_DETAIL_LEVELS, \
    DEFAULT_LOG_DETAIL_LEVEL

from ._context_obj import ContextObj
from ._common import GENERAL_OPTIONS_METAVAR, TABLE_FORMATS, \
    CIM_OBJECT_OUTPUT_FORMATS, warning_msg
from ._pywbem_server import PywbemServer
from .config import DEFAULT_OUTPUT_FORMAT, DEFAULT_NAMESPACE, \
    PYWBEMCLI_PROMPT, PYWBEMCLI_HISTORY_FILE, DEFAULT_MAXPULLCNT, \
    DEFAULT_CONNECTION_TIMEOUT, MAX_TIMEOUT

from ._connection_repository import ConnectionRepository

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
@click.option('-n', '--name', type=str, metavar='NAME',
              # defaulted in code
              envvar=PywbemServer.name_envvar,
              help='Use the WBEM server defined by the WBEM connection '
                   'definition NAME. '
                   'This option is mutually exclusive with the --server '
                   'and --name options, since each defines a WBEM server. '
                   'Default: EnvVar {ev}, or none.'.
                   format(ev=PywbemServer.name_envvar))
@click.option('-m', '--mock-server', type=str, multiple=True, metavar="FILE",
              # defaulted in code
              envvar=PywbemServer.mock_server_envvar,
              help='Use a mock WBEM server that is automatically created in '
                   'pywbemcli and populated with CIM objects that are defined '
                   'in the specified MOF file or Python script file. '
                   'See the pywbemcli documentation for more information. '
                   'This option may be specified multiple times, and is '
                   'mutually exclusive with the --server and --name options, '
                   'since each defines a WBEM server. '
                   'Default: EnvVar {ev}, or none.'.
                   format(ev=PywbemServer.mock_server_envvar))
@click.option('-s', '--server', type=str, metavar='URL',
              # defaulted in code
              envvar=PywbemServer.server_envvar,
              help='Use the WBEM server at the specified URL with format: '
                   '[SCHEME://]HOST[:PORT]. '
                   'SCHEME must be "https" (default) or "http". '
                   'HOST is a short or long hostname or literal IPV4/v6 '
                   'address. '
                   'PORT defaults to 5989 for https and 5988 for http. '
                   'This option is mutually exclusive with the --mock-server '
                   'and --name options, since each defines a WBEM server. '
                   'Default: EnvVar {ev}, or none.'.
                   format(ev=PywbemServer.server_envvar))
@click.option('-u', '--user', type=str, metavar='TEXT',
              # defaulted in code
              envvar=PywbemServer.user_envvar,
              help='User name for the WBEM server. '
                   'Default: EnvVar {ev}, or none.'.
                   format(ev=PywbemServer.user_envvar))
@click.option('-p', '--password', type=str, metavar='TEXT',
              # defaulted in code
              envvar=PywbemServer.password_envvar,
              help='Password for the WBEM server. '
                   'Default: EnvVar {ev}, or prompted for if --user specified.'.
                   format(ev=PywbemServer.password_envvar))
@click.option('-N', '--no-verify', is_flag=True,
              # defaulted in code
              envvar=PywbemServer.no_verify_envvar,
              help='If true, client does not verify the X.509 server '
                   'certificate presented by the WBEM server during TLS/SSL '
                   'handshake. '
                   'Default: EnvVar {ev}, or false.'.
                   format(ev=PywbemServer.no_verify_envvar))
@click.option('--ca-certs', type=str, metavar="FILE",
              # defaulted in code
              envvar=PywbemServer.ca_certs_envvar,
              help='Path name of a file or directory containing certificates '
                   'that will be matched against the server certificate '
                   'presented by the WBEM server during TLS/SSL handshake. '
                   'Default: EnvVar {ev}, or [{dirs}].'.
                   format(ev=PywbemServer.ca_certs_envvar,
                          dirs=', '.join(DEFAULT_CA_CERT_PATHS)))
@click.option('-c', '--certfile', type=str, metavar="FILE",
              # defaulted in code
              envvar=PywbemServer.certfile_envvar,
              help='Path name of a PEM file containing a X.509 client '
                   'certificate that is used to enable TLS/SSL 2-way '
                   'authentication by presenting the certificate to the '
                   'WBEM server during TLS/SSL handshake. '
                   'Default: EnvVar {ev}, or none.'.
                   format(ev=PywbemServer.certfile_envvar))
@click.option('-k', '--keyfile', type=str, metavar='FILE',
              # defaulted in code
              envvar=PywbemServer.keyfile_envvar,
              help='Path name of a PEM file containing a X.509 private key '
                   'that belongs to the certificate in the --certfile file. '
                   'Not required if the private key is part of the '
                   '--certfile file. '
                   'Default: EnvVar {ev}, or none.'.
                   format(ev=PywbemServer.keyfile_envvar))
@click.option('-t', '--timeout', type=click.IntRange(0, MAX_TIMEOUT),
              metavar='INT',
              # defaulted in code
              envvar=PywbemServer.timeout_envvar,
              help='Client-side timeout in seconds for operations with the '
                   'WBEM server. '
                   'Default: EnvVar {ev}, or {default}.'.
                   format(ev=PywbemServer.timeout_envvar,
                          default=DEFAULT_CONNECTION_TIMEOUT))
@click.option('-U', '--use-pull', type=click.Choice(['yes', 'no', 'either']),
              # defaulted in code
              envvar=PywbemServer.use_pull_envvar,
              help='Determines whether pull operations are used for '
                   'operations with the WBEM server that return lists of '
                   'instances, as follows: '
                   '"yes" uses pull operations and fails if not supported by '
                   'the server; '
                   '"no" uses traditional operations; '
                   '"either" (default) uses pull operations if supported by '
                   'the server, and otherwise traditional operations. '
                   'Default: EnvVar {ev}, or "either".'.
                   format(ev=PywbemServer.use_pull_envvar))
@click.option('--pull-max-cnt', type=int, metavar='INT',
              # defaulted in code
              envvar=PywbemServer.pull_max_cnt_envvar,
              help='Maximum number of instances to be returned by the WBEM '
                   'server in each open or pull response, if pull operations '
                   'are used. '
                   'This is a tuning parameter that does not affect the '
                   'external behavior of the commands. '
                   'Default: EnvVar {ev}, or {default}'.
                   format(ev=PywbemServer.pull_max_cnt_envvar,
                          default=DEFAULT_MAXPULLCNT))
@click.option('-T', '--timestats', is_flag=True,
              # defaulted in code
              help='Show time statistics of WBEM server operations.')
@click.option('-d', '--default-namespace', type=str, metavar='NAMESPACE',
              # defaulted in code
              envvar=PywbemServer.defaultnamespace_envvar,
              help='Default namespace, to be used when commands do not '
                   'specify the --namespace command option. '
                   'Default: EnvVar {ev}, or {default}.'.
                   format(ev=PywbemServer.defaultnamespace_envvar,
                          default=DEFAULT_NAMESPACE))
@click.option('-o', '--output-format', metavar='FORMAT',
              # defaulted in code
              help='Output format for the command result. '
                   'The specified format may be overriden since not all '
                   'formats apply to all result data types. '
                   'FORMAT is a table format [{tb}] or object format [{ob}]. '
                   'Default: {default}.'.
                   format(tb='|'.join(TABLE_FORMATS),
                          ob='|'.join(CIM_OBJECT_OUTPUT_FORMATS),
                          default=DEFAULT_OUTPUT_FORMAT))
@click.option('-l', '--log', type=str, metavar='COMP[=DEST[:DETAIL]],...',
              # defaulted in code
              envvar=PywbemServer.log_envvar,
              help='Enable logging of the WBEM operations, defined by a list '
                   'of log configuration strings with: '
                   'COMP: [{comp_choices}]; '
                   'DEST: [{dest_choices}], default: {dest_default}; '
                   'DETAIL: [{detail_choices}], default: {detail_default}. '
                   'Default: EnvVar {ev}, or {default}.'.
                   format(comp_choices='|'.join(LOGGER_SIMPLE_NAMES),
                          dest_choices='|'.join(LOG_DESTINATIONS),
                          dest_default=DEFAULT_LOG_DESTINATION,
                          detail_choices='|'.join(LOG_DETAIL_LEVELS),
                          detail_default=DEFAULT_LOG_DETAIL_LEVEL,
                          ev=PywbemServer.log_envvar,
                          default='all'))
@click.option('-v', '--verbose', is_flag=True,
              default=False,
              help='Display extra information about the processing.')
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

    Pywbemcli implements command groups and commands to execute the CIM-XML
    operations defined by the DMTF CIM Operations Over HTTP specification
    (DSP0200).

    The general options shown below can also be specified on any of the
    commands, positioned right after the 'pywbemcli' command name.

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

        if keyfile and not certfile:
            click.echo('The --keyfile option "%s" is allowed only if the '
                       '--certfile option is also used' % keyfile, err=True)
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
                    'Invalid choice for --use-pull %s' % use_pull)
        else:
            resolved_use_pull = DEFAULT_PULL_CHOICE

        resolved_pull_max_cnt = pull_max_cnt or DEFAULT_MAXPULLCNT

        resolved_timeout = timeout or DEFAULT_CONNECTION_TIMEOUT

        # Create the PywbemServer object (this contains all of the info
        # for the connection defined by the cmd line input)
        if server or mock_server:
            if name:
                click.echo('Option conflict: --name "%s" conflicts with '
                           'existence of --server and --mock-server' %
                           name, err=True)
                raise click.Abort()
            name = 'not-saved'
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
            connections = ConnectionRepository()
            s_name = None
            if name:
                if name in connections:
                    s_name = name
                # exception when defined name does not exist
                else:
                    raise click.ClickException('Named connection "{}" does '
                                               'not exist and no --server or '
                                               '--mock-server options to '
                                               'define a '
                                               'WBEM server'.format(name))
            else:  # no --name option
                # get any persistent default_connection name
                s_name = connections.get_default_connection()

                if s_name and s_name not in connections:
                    click.echo('Invalid selected connection "%s". This name '
                               'not in connections repository. Deleting',
                               err=True)
                    connections.set_default_connection(None)
                    raise click.Abort()

            # Get the named connection from the repo
            if s_name:
                pywbem_server = connections[s_name]
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
                        warning_msg('"%s %s" ignored when "-n/--name  or '
                                    'default name used' %
                                    (option[1], option[0]))
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
            resolved_pull_max_cnt = ctx.obj.pull_max_cnt
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
    click.echo("""
The following can be entered in interactive mode:

  COMMAND                     Execute pywbemcli command COMMAND.
  !SHELL-CMD                  Execute shell command SHELL-CMD.
  <CTRL-D>, :q, :quit, :exit  Exit interactive mode.
  <TAB>                       Tab completion (can be used anywhere).
  -h, --help                  Show pywbemcli general help message, including a
                              list of pywbemcli commands.
  COMMAND --help              Show help message for pywbemcli command COMMAND.
  help                        Show this help message.
  :?, :h, :help               Show help message about interactive mode.
  <UP>, <DOWN>                Scroll through pwbemcli command history.
""")


@cli.command('repl')
@click.pass_context
def repl(ctx):
    """
    Enter interactive mode (default).

    Enter the interactive mode where pywbemcli commands can be entered
    interactively. The prompt is changed to 'pywbemcli>'.

    Command history is supported. The command history is stored in a file
    ~/.pywbemcli_history.

    Pywbemcli may be terminated from this mode by entering
    <CTRL-D>, :q, :quit, :exit
    """

    history_file = PYWBEMCLI_HISTORY_FILE
    if history_file.startswith('~'):
        history_file = os.path.expanduser(history_file)

    click.echo("Enter 'help' for help, <CTRL-D> or ':q' to exit pywbemcli.")

    prompt_kwargs = {
        'message': PYWBEMCLI_PROMPT,
        'history': FileHistory(history_file),
    }
    click_repl.repl(ctx, prompt_kwargs=prompt_kwargs)
