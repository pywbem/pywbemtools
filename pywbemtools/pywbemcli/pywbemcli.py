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

from __future__ import absolute_import, print_function

import os
import sys
import traceback
from copy import deepcopy
import click
import click_repl
from prompt_toolkit.history import FileHistory
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory

import pywbem
from pywbem import LOGGER_SIMPLE_NAMES, \
    LOG_DESTINATIONS, DEFAULT_LOG_DESTINATION, LOG_DETAIL_LEVELS, \
    DEFAULT_LOG_DETAIL_LEVEL

from ._context_obj import ContextObj, display_click_context
from ._common import GENERAL_OPTS_TXT, SUBCMD_HELP_TXT, TABLE_FORMATS, \
    CIM_OBJECT_OUTPUT_FORMATS
from ._common_options import add_options, help_option
from ._pywbem_server import PywbemServer
from .config import DEFAULT_NAMESPACE, \
    PYWBEMCLI_PROMPT, PYWBEMCLI_HISTORY_FILE, DEFAULT_MAXPULLCNT, \
    DEFAULT_CONNECTION_TIMEOUT, MAX_TIMEOUT, USE_AUTOSUGGEST
from ._connection_repository import ConnectionRepository
from ._click_extensions import PywbemcliTopGroup

__all__ = ['cli']

PYWBEM_VERSION = "pywbem, version {}".format(pywbem.__version__)

# Defaults for some options
DEFAULT_VERIFY = True  # The default is to verify
DEFAULT_TIMESTATS = False
DEFAULT_PULL_CHOICE = 'either'
USE_PULL_CHOICE = {'either': None, 'yes': True, 'no': False}

TERMWIDTH_ENVVAR = os.getenv(PywbemServer.termwidth_envvar, None)
if TERMWIDTH_ENVVAR:
    try:
        TERMWIDTH_ENVVAR = int(TERMWIDTH_ENVVAR)
    except ValueError:
        TERMWIDTH_ENVVAR = None

CONTEXT_SETTINGS = dict(

    # Enable -h as additional help option:
    help_option_names=['-h', '--help'],

    # Default the output width properly:
    terminal_width=TERMWIDTH_ENVVAR or click.get_terminal_size()[0],
)


# pylint: disable=bad-continuation
# PywbemcliTopGroup sets order commands listed in help output
@click.group(invoke_without_command=True, cls=PywbemcliTopGroup,
             context_settings=CONTEXT_SETTINGS,
             options_metavar=GENERAL_OPTS_TXT,
             subcommand_metavar=SUBCMD_HELP_TXT)
@click.option('-n', '--name', 'svr_name', type=str, metavar='NAME',
              # defaulted in code
              envvar=PywbemServer.name_envvar,
              help='Use the WBEM server defined by the WBEM connection '
                   'definition NAME. '
                   'This option is mutually exclusive with the --server and '
                   '--mock-server options, since each defines a WBEM server. '
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
@click.option('--verify/--no-verify', 'verify', default=None,
              # defaulted in code
              envvar=PywbemServer.verify_envvar,
              help='If --verify, client verifies the X.509 server '
                   'certificate presented by the WBEM server during TLS/SSL '
                   'handshake. If --no-verify client bypasses verification. '
                   'Default: EnvVar {ev}, or "--verify".'.
                   format(ev=PywbemServer.verify_envvar))
@click.option('--ca-certs', type=str, metavar="CACERTS",
              default=None,  # defaulted in code
              envvar=PywbemServer.ca_certs_envvar,
              help='Certificates to be used for validating the certificate '
                   'presented by the WBEM server during TLS/SSL handshake: '
                   'FILE: Use the certs in the specified PEM file; '
                   'DIR: Use the certs in the PEM files in the specified '
                   'directory; '
                   '"certifi" (pywbem 1.0 or later): Use the certs provided by '
                   'the certifi Python package; '
                   'Default: EnvVar {ev}, or "certifi" (pywbem 1.0 or later), '
                   'or the certs in the PEM files in the first existing '
                   'directory from from a list of system directories '
                   '(pywbem before 1.0).'.
                   format(ev=PywbemServer.ca_certs_envvar))
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
              default=None,
              envvar=PywbemServer.defaultnamespace_envvar,
              help='Default namespace, to be used when commands do not '
                   'specify the --namespace command option. '
                   'Default: EnvVar {ev}, or {default}.'.
                   format(ev=PywbemServer.defaultnamespace_envvar,
                          default=DEFAULT_NAMESPACE))
@click.option('-o', '--output-format', metavar='FORMAT',
              help='Output format for the command result. '
                   'The default and allowed output formats are command '
                   'specific. '
                   'The default output_format is None so that each command '
                   'selects its own default format. '
                   'FORMAT is either a table format: [{tb}] or CIM object '
                   'format: [{ob}].'.
                   format(tb='|'.join(TABLE_FORMATS),
                          ob='|'.join(CIM_OBJECT_OUTPUT_FORMATS)))
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
@click.option('-v', '--verbose/--no-verbose',
              default=None,
              help='Display extra information about the processing.')
@click.option('--pdb', is_flag=True,
              # defaulted in code
              envvar=PywbemServer.pdb_envvar,
              help='Pause execution in the built-in pdb debugger just before '
                   'executing the command within pywbemcli. '
                   'Default: EnvVar {ev}, or false.'.
                   format(ev=PywbemServer.pdb_envvar))
@click.version_option(
    message='%(prog)s, version %(version)s\n' + PYWBEM_VERSION,
    help='Show the version of this command and the pywbem package.')
@add_options(help_option)
@click.pass_context
def cli(ctx, server, svr_name, default_namespace, user, password, timeout,
        verify, certfile, keyfile, ca_certs, output_format, use_pull,
        pull_max_cnt, mock_server, verbose=None, timestats=None, log=None,
        pdb=None):
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

    The width of help texts of this command can be set with the
    PYWBEMCLI_TERMWIDTH environment variable.

    For more detailed documentation, see:

        https://pywbemtools.readthedocs.io/en/stable/
    """
    # list of options that are not allowed in some cases:
    # i.e. When -name is used and when in interactive mode.
    resolved_mock_server = []
    conditional_options = ((default_namespace, 'default_namespace'),
                           (timeout, 'timeout'),
                           (verify, 'verify'),
                           (user, 'user'),
                           (certfile, 'certfile'),
                           (keyfile, 'keyfile'),
                           (ca_certs, 'ca_certs'),
                           (server, 'server'),
                           # Special because we remove some items from the
                           # list of mocks that define the mock repository
                           (resolved_mock_server, 'mock-server'))

    def create_server_instance(svr_name):
        """
        Create a PywbemServer instance from the cli arguments and return
        that object.  This method depends on using variables from the
        enclosing function. If the arguments to create a server do not exist
        no server is created.
        NOTE: svr_name passed to this function because the ClickException
        treats it as a reference before assignment if using the svr_name
        from the enclosing scopt
        """
        # test for conflicting server definitions.
        if server or resolved_mock_server:
            if svr_name:
                click.ClickException('Option conflict: --name "{}" '
                                     'conflicts with existence of --server and '
                                     '--mock-server'.format(svr_name))
            svr_name = 'not-saved'
            pywbem_server = PywbemServer(server,
                                         resolved_default_namespace,
                                         name=svr_name,
                                         user=user,
                                         password=password,
                                         timeout=resolved_timeout,
                                         use_pull=resolved_use_pull,
                                         verify=resolved_verify,
                                         certfile=certfile,
                                         keyfile=keyfile,
                                         ca_certs=resolved_ca_certs,
                                         mock_server=resolved_mock_server)
        else:  # Server and mock_server were not specified
            # if name cmd line option, get connection repo and
            # get name from the repo.
            connections = ConnectionRepository()
            local_svr_name = None
            if svr_name:
                if svr_name not in connections:
                    raise click.ClickException(
                        "Connection definition '{}' not found in "
                        "connections file '{}'".
                        format(svr_name, connections.connections_file))
                local_svr_name = svr_name
            else:  # no connection name specified
                # get the default_connection definition
                local_svr_name = connections.get_default_connection_name()
                # Abort here because we have modified the file to clear
                # the bad default. First this should never happen and
                # second, if it does, Abort seems logical.
                if local_svr_name and local_svr_name not in connections:
                    connections.set_default_connection(None)
                    click.echo(
                        "Default connection definition '{}' not found in "
                        "connections file '{}'; deleted default connection "
                        "in connections file".
                        format(local_svr_name, connections.connections_file),
                        err=True)
                    raise click.Abort()
                if verbose:
                    click.echo('Current connection: "{}"'
                               .format(local_svr_name))

            # Get the named connection from the repo
            if local_svr_name:
                pywbem_server = connections[local_svr_name]
                # Test for invalid options with the --name option
                for option in conditional_options:
                    if option[0]:
                        raise click.ClickException(
                            '"--{} {}" option invalid when --name exists or '
                            'default name set.'.format(option[1], option[0]))

            else:
                # If no server defined, set None to allow commands that
                # do not require a server to be executed with no server
                # defined.
                pywbem_server = None
        return pywbem_server

    # Process cli options to produce resolved options, i.e. the
    # options with any defaults applied for non None options.
    # Produces new variables resolved... so that later tests can confirm that
    # original variables were None or not None
    pywbem_server = None
    resolved_default_namespace = default_namespace or DEFAULT_NAMESPACE
    resolved_timestats = timestats or DEFAULT_TIMESTATS
    resolved_verify = DEFAULT_VERIFY if verify is None else verify
    resolved_ca_certs = ca_certs  # None should be passed on

    if server and svr_name:
        raise click.ClickException(
            'Conflicting server definitions: name: {}, server: {}'.
            format(svr_name, server))

    if keyfile and not certfile:
        raise click.ClickException(
            'The --keyfile option "{}" is allowed only if the --certfile '
            'option is also used'.format(keyfile))
    # process mock_server option
    if mock_server:
        assert isinstance(mock_server, tuple)
        # resolve relative and absolute paths
        mock_server_path = []
        for fn in mock_server:
            if fn == os.path.basename(fn):
                mock_server_path.append(os.path.join(os.getcwd(), fn))
            else:
                mock_server_path.append(fn)

        # Test for non-existent files
        # TODO: Future: Create common method with code in build_respository
        for file_path in mock_server_path:
            ext = os.path.splitext(file_path)[1]
            if ext not in ['.py', '.mof']:
                raise click.ClickException(
                    "Mock file '{}' has invalid suffix '{}' "
                    "- must be '.py' or '.mof'".format(file_path, ext))
            if not os.path.isfile(file_path):
                raise click.ClickException(
                    "Mock file '{}' does not exist".format(file_path))
            if ext != '.py':
                resolved_mock_server.append(file_path)
                continue

            # The following allows executing selected python scripts at
            # startup but with only VERBOSE as a known global.  Inserted
            # primarily to support testing. If the flag exists in the
            # file, it executes immediatly but does not put into mock_server
            # variable
            with open(file_path) as fp:
                if '!PROCESS!AT!STARTUP!' in fp.readline():
                    file_source = fp.read()
                    # Only verbose is allowed here
                    globalparams = {'VERBOSE': verbose}
                    try:
                        # Using compile+exec instead of just exec allows
                        # specifying the file name, causing it to appear in
                        # any tracebacks.
                        file_code = compile(file_source, file_path, 'exec')
                        # pylint: disable=exec-used
                        exec(file_code, globalparams, None)
                    except Exception:
                        exc_type, exc_value, exc_traceback = sys.exc_info()
                        tb = traceback.format_exception(exc_type, exc_value,
                                                        exc_traceback)
                        click.echo(
                            "Mock Python process-at-startup script '{}' "
                            "failed:\n{}".format(file_path, "\n".join(tb)),
                            err=True)
                        raise click.Abort()
                else:  # not processed during startup
                    resolved_mock_server.append(file_path)

    # Simultaneous mock_server and server fails
    if server and resolved_mock_server:
        raise click.ClickException(
            'Conflicting server definitions: server: {}, mock-server: {}'.
            format(server, ', '.join(resolved_mock_server)))

    # simultaneous mock_server and svr_name fails. Note: resolve mock_server
    # does not include any mocks processedatstartup
    if resolved_mock_server and svr_name:
        raise click.ClickException(
            'Conflicting server definitions: mock-server: {}, name: {}'.
            format(', '.join(resolved_mock_server), svr_name))

    # set pull default if necessary and create the resolved variable
    use_pull = use_pull or DEFAULT_PULL_CHOICE
    resolved_use_pull = USE_PULL_CHOICE[use_pull]

    resolved_pull_max_cnt = pull_max_cnt or DEFAULT_MAXPULLCNT

    resolved_timeout = timeout or DEFAULT_CONNECTION_TIMEOUT

    # Command mode (ctx is None). Processes command on comand line and quits
    # Apply the documented option defaults to create a pywbem_server instance
    # and a ContextObj instance
    if ctx.obj is None:  # No context. This is cmd line mode
        # Create the PywbemServer object (this contains all of the info
        # for the connection defined by the cmd line input)
        pywbem_server = create_server_instance(svr_name)

    # Interactive mode cmd line processing (ctx not Nome)
    # In interactive mode, general options specified in cmd line are used
    # to modify the pywbem_server object and the general options
    # for a single command execution.
    # This requires being able to determine for each option whether it has been
    # specified and is why general options don't define defaults in the
    # decorators that define them.
    else:  # ctx.obj exists. Processing an interactive command.
        # Apply the option defaults from the command line options
        # or from the context object.

        # If --name option, get server from connection
        if svr_name:
            connections = ConnectionRepository()
            try:
                pywbem_server = connections[svr_name]
            except KeyError:
                raise click.ClickException(
                    "Connection definition '{}' not found in "
                    "connections file '{}'".
                    format(svr_name, connections.connections_file))

        # If other parameters, modify the existing connection and reset it.
        # TODO: refactor this code to avoid deepcopy when not needed.
        else:
            if pywbem_server is None:
                # Copy to keep the original clean from any changes
                pywbem_server = deepcopy(ctx.obj.pywbem_server)
            if pywbem_server:
                modified_server = False
                if server:
                    if pywbem_server.mock_server:
                        pywbem_server.mock_server = []
                    pywbem_server.server = server
                    modified_server = True
                if mock_server:
                    if pywbem_server.server:
                        pywbem_server.server = None
                    pywbem_server.mock_server = resolved_mock_server
                    modified_server = True
                if user:
                    pywbem_server.user = user
                    modified_server = True
                if password:
                    pywbem_server.password = password
                    modified_server = True
                if verify is not None:
                    pywbem_server.verify = resolved_verify
                    modified_server = True
                if ca_certs:
                    pywbem_server.ca_certs = ca_certs
                    modified_server = True
                if certfile:
                    pywbem_server.certfile = certfile
                    modified_server = True
                if keyfile:
                    pywbem_server.keyfile = keyfile
                    modified_server = True
                if timeout:
                    pywbem_server.timeout = resolved_timeout
                if use_pull:
                    pywbem_server.use_pull = resolved_use_pull
                if server:
                    pywbem_server.server = server
                    modified_server = True
                if default_namespace:
                    pywbem_server.default_namespace = resolved_default_namespace
                    modified_server = True
                if modified_server:
                    pywbem_server.reset()
                else:
                    pywbem_server = ctx.obj.pywbem_server
            else:
                pywbem_server = create_server_instance(svr_name)

        # The following variables are maintained only in the context_obj and
        # not attached to any particular connection. If the cli argument is
        # None, this argument was not defined as part of this interactive
        # command
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
        if pdb is None:
            pdb = ctx.obj.pdb

    # Create a command context for each command: An interactive command has
    # its own command context as a child of the command context for the
    # command line.
    ctx.obj = ContextObj(pywbem_server, output_format,
                         resolved_use_pull,
                         resolved_pull_max_cnt,
                         resolved_timestats,
                         log, verbose, pdb)
    if verbose and os.getenv('PYWBEMCLI_DIAGNOSTICS'):
        print('CONTEXT_OBJ {!r}'.format(ctx.obj))
        print('CLICK CTX {}'.format(ctx))
        display_click_context(ctx, msg="After adding Context",
                              display_attrs=True)
    # Invoke command if one exists.
    if ctx.invoked_subcommand is None:
        ctx.invoke(repl)


@cli.command('help', options_metavar=GENERAL_OPTS_TXT)
@add_options(help_option)
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

  COMMAND: May be two words (class enumerate) for commands that are within
  a group or a single word for special commands like `repl` that are not in
  a group.
""")


@cli.command('repl', options_metavar=GENERAL_OPTS_TXT)
@add_options(help_option)
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

    if USE_AUTOSUGGEST:
        prompt_kwargs['auto_suggest'] = AutoSuggestFromHistory()

    click_repl.repl(ctx, prompt_kwargs=prompt_kwargs)
