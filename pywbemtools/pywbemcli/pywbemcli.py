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
import io
import sys
import traceback
from copy import deepcopy
import warnings
import click
import click_repl
from prompt_toolkit.history import FileHistory
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory

from pywbem import LOGGER_SIMPLE_NAMES, \
    LOG_DESTINATIONS, DEFAULT_LOG_DESTINATION, LOG_DETAIL_LEVELS, \
    DEFAULT_LOG_DETAIL_LEVEL
from pywbem import __version__ as pywbem_version

from ._context_obj import ContextObj, display_click_context
from ._common import GENERAL_OPTS_TXT, SUBCMD_HELP_TXT, OUTPUT_FORMAT_GROUPS
from ._common_options import add_options, help_option
from ._pywbem_server import PywbemServer
from .config import DEFAULT_NAMESPACE, PYWBEMCLI_PROMPT, \
    PYWBEMCLI_HISTORY_FILE, DEFAULT_MAXPULLCNT, DEFAULT_CONNECTION_TIMEOUT, \
    MAX_TIMEOUT, USE_AUTOSUGGEST
from ._connection_repository import ConnectionRepository, \
    ConnectionsFileError
from ._click_extensions import PywbemcliTopGroup
from ._utils import pywbemcliwarn, get_terminal_width, CONNECTIONS_FILENAME, \
    DEFAULT_CONNECTIONS_FILE


__all__ = ['cli']

PYWBEMCLI_STARTUP_ENVVAR = "PYWBEMCLI_STARTUP_SCRIPT"


# Defaults for some options
DEFAULT_VERIFY = True  # The default is to verify
DEFAULT_PULL_CHOICE = 'either'
USE_PULL_CHOICE = {'either': None, 'yes': True, 'no': False, 'default': None}

#
# Context variables passed to click
#
CONTEXT_SETTINGS = dict(

    # Enable -h as additional help option:
    help_option_names=['-h', '--help'],

    # Default the output width properly:
    terminal_width=get_terminal_width(),
)

###########################################################################
#
# Support functions for the the cli(...) function
#
###########################################################################


def _validate_connection_name(connections_repo, connection_name):
    """
    Validate that connection name exists in the connection_repo and that
    the connection name can be retrieved.

    Returns:
        PywbemServer object that defines connection if found in connections_file

    Raises:
        click.ClickException - connection not found
        ConnectionsFileError - Connections file invalid
    """
    try:
        pywbem_server = connections_repo[connection_name]
        return pywbem_server

    except KeyError:
        raise click.ClickException(
            'Connection definition "{}" not found in connections '
            'file "{}"'.
            format(connection_name, connections_repo.connections_file))

    except ConnectionsFileError as cfe:
        click.echo('Fatal error: {0}: {1}'.
                   format(cfe.__class__.__name__, cfe),
                   err=True)
        raise click.Abort()


def _validate_connections_file(connections_repo, abort=False):
    """
    Test for existence of a connections file.
    Abort click if file does not exist and abort is True.  If it does not exist
    and abort is False, execute ClickException
    """
    if not connections_repo.file_exists():
        if abort:
            click.echo('Connections file does not exist: {}'.format(
                connections_repo.connections_file), err=True)
            raise click.Abort()

        raise click.ClickException(
            'Connections file does not exist: {}'.format(
                connections_repo.connections_file))


def _execute_startup_script(file_path, verbose):
    """
    Execute the python script. This  executes the script defined in file_path.
    The purpose of this code is to execute test scripts at startup.
    """

    ext = os.path.splitext(file_path)[1]
    if ext not in ['.py']:
        raise click.ClickException(
            "File '{}' has invalid suffix '{}' "
            "- must be '.py'".format(file_path, ext))
    if not os.path.isfile(file_path):
        raise click.ClickException(
            "File '{}' does not exist".format(file_path))

    with io.open(file_path, 'r', encoding='utf-8') as fp:
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
                "Python test process-at-startup script '{}' "
                "failed:\n{}".format(file_path, "\n".join(tb)),
                err=True)
            raise click.Abort()


def _resolve_mock_server(mock_server):
    """
    Validate and resolve the mock_server parameter.
    Validates that all files defined in the server exist and that the
    types are valid.

    Parameters:

      mock_server (tuple of string):
        Strings defining all of the files that compromise the mock_server
        definiton.

    Returns: list of resolved mock server definition components derived
       from the input parameter mock_server.

    Raises:
      click.ClickException for any errors.
    """
    resolved_mock_server = []
    assert isinstance(mock_server, tuple)
    # Normalize paths for different OS's
    mock_server_path = [os.path.normpath(fn) for fn in mock_server]

    # Test for valid file types and existence for mock_server files.
    for file_path in mock_server_path:
        ext = os.path.splitext(file_path)[1]
        if ext not in ['.py', '.mof']:
            raise click.ClickException(
                "Mock file '{}' has invalid suffix '{}' "
                "- must be '.py' or '.mof'".format(file_path, ext))
        if not os.path.isfile(file_path):
            raise click.ClickException(
                "Mock file '{}' does not exist".format(file_path))
        resolved_mock_server.append(file_path)
    return resolved_mock_server


def _set_default_if_empty_str(tst_str, default=None):
    """
    Return None if str is an empty string or return str. Used to test for
    general options that reset with value of "" and reset to either None
    or the default value.

    Parameters:
      tst_str (:term:1string):
        the string to test for value of ""

      default (:term:`string`):
        Optional default string value to return

    Returns:
        None or the value of the default parameter
    """
    return default if tst_str == "" else tst_str


def _validate_no_server_option_conficts(server, connection_name, mock_server):
    """
    Validate that only one of the general options server, connection_name,
    or resolved_mock_server contains data since only one is allowed as the
    means to define a server.

    Raises:
      click.ClickException if more that one of the defined parameters is not
      None.
    """
    if server and connection_name:
        raise click.ClickException(
            'Conflicting server definitions: name: {}, server: {}'.
            format(connection_name, server))

    # Simultaneous mock_server and server fails
    if server and mock_server:
        raise click.ClickException(
            'Conflicting server definitions: server: {}, mock-server: {}'.
            format(server, ', '.join(mock_server)))

    # Simultaneous mock_server and connection_name: Generate Exception.
    if mock_server and connection_name:
        raise click.ClickException(
            'Conflicting server definitions: mock-server: {}, name: {}'.
            format(', '.join(mock_server), connection_name))


def _create_server_instance(server, connection_name, resolved_default_namespace,
                            user, password, resolved_timeout,
                            resolved_use_pull, resolved_pull_max_cnt,
                            resolved_verify,
                            certfile, keyfile, resolved_ca_certs,
                            resolved_mock_server, connections_repo,
                            conditional_options,
                            verbose):
    """
    Create a PywbemServer instance from the cli arguments and return
    that object.  This method depends on using variables from the
    enclosing function. If the arguments to create a server do not exist
    no server is created.

    This method used only during pywbemcli statup to process initial
    general options and when interactive mode sets new server from the
    --name option.

    NOTE: connection_name is passed to this function because the
    ClickException treats it as a reference before assignment if using the
    connection_name from the enclosing scope.
    """
    if server or resolved_mock_server:
        connection_name = 'not-saved'
        pywbem_server = PywbemServer(server,
                                     resolved_default_namespace,
                                     name=connection_name,
                                     user=user,
                                     password=password,
                                     timeout=resolved_timeout,
                                     use_pull=resolved_use_pull,
                                     pull_max_cnt=resolved_pull_max_cnt,
                                     verify=resolved_verify,
                                     certfile=certfile,
                                     keyfile=keyfile,
                                     ca_certs=resolved_ca_certs,
                                     mock_server=resolved_mock_server)
    else:  # Server and mock_server were not specified
        # If name cmd line option, get get name from the connections
        # repo or use default name if it exists.
        if connection_name:
            _validate_connections_file(connections_repo, abort=True)
            _validate_connection_name(connections_repo, connection_name)

        # No connection name specified, try default connection name from
        # connections file
        else:
            # Get the default_connection definition
            try:
                if connections_repo.file_exists():
                    connection_name = \
                        connections_repo.default_connection_name

                    # Test if the default connection name is actually
                    # in the repo.  If not reset the default connection
                    # name to None and continue.
                    # This should never occur unless connection file
                    # is corrupted.
                    if connection_name and connection_name not in \
                            connections_repo:
                        connections_repo.default_connection_name = None
                        raise click.ClickException(
                            'Default connection name: "{}" not found in '
                            'connections file "{}"; default connection '
                            'name is cleared.'.
                            format(connection_name,
                                   connections_repo.connections_file))
                    if verbose:
                        click.echo('Current connection: "{}"'
                                   .format(connection_name))
            except ConnectionsFileError as cfc:
                click.echo("{}, {}". format(cfc.__class__.__name__, cfc),
                           err=True)
                raise click.Abort()

        # Get the named connection from the connections repo
        if connection_name:
            pywbem_server = connections_repo[connection_name]
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


############################################################################
#
#   cli command (main entry point) and definition of all of the pywbemcli
#   general options.
#
############################################################################


# pylint: disable=bad-continuation
# PywbemcliTopGroup sets order commands listed in help output
@click.group(invoke_without_command=True, cls=PywbemcliTopGroup,
             context_settings=CONTEXT_SETTINGS,
             options_metavar=GENERAL_OPTS_TXT,
             subcommand_metavar=SUBCMD_HELP_TXT)
@click.option('-n', '--name', 'connection_name', type=str, metavar='NAME',
              # defaulted in code
              envvar=PywbemServer.name_envvar,
              help=u'Use the WBEM server defined by the WBEM connection '
                   u'definition NAME. '
                   u'This option is mutually exclusive with the --server and '
                   u'--mock-server options, since each defines a WBEM server. '
                   u'Default: EnvVar {ev}, or none.'.
                   format(ev=PywbemServer.name_envvar))
@click.option('-m', '--mock-server', type=str, multiple=True, metavar="FILE",
              # defaulted in code
              envvar=PywbemServer.mock_server_envvar,
              help=u'Use a mock WBEM server that is automatically created in '
                   u'pywbemcli and populated with CIM objects that are defined '
                   u'in the specified MOF file or Python script file. The '
                   u'files may be specified with relative or absolute path.'
                   u'See the pywbemcli documentation for more information. '
                   u'This option may be specified multiple times, and is '
                   u'mutually exclusive with the --server and --name options, '
                   'since each defines a WBEM server. '
                   'Default: EnvVar {ev}, or none.'.
                   format(ev=PywbemServer.mock_server_envvar))
@click.option('-s', '--server', type=str, metavar='URL',
              # defaulted in code
              envvar=PywbemServer.server_envvar,
              help=u'Use the WBEM server at the specified URL with format: '
                   u'[SCHEME://]HOST[:PORT]. '
                   u'SCHEME must be "https" (default) or "http". '
                   u'HOST is a short or long hostname or literal IPV4/v6 '
                   u'address. '
                   u'PORT defaults to 5989 for https and 5988 for http. '
                   u'This option is mutually exclusive with the --mock-server '
                   u'and --name options, since each defines a WBEM server. '
                   u'Default: EnvVar {ev}, or none.'.
                   format(ev=PywbemServer.server_envvar))
@click.option('-u', '--user', type=str, metavar='TEXT',

              default=None,  # There is no default value
              envvar=PywbemServer.user_envvar,
              help=u'User name for the WBEM server.  Use "" to set default in '
                   u'interactive mode.'
                   u'Default: EnvVar {ev}, or none.'.
                   format(ev=PywbemServer.user_envvar))
@click.option('-p', '--password', type=str, metavar='TEXT',
              default=None,  # There is not default value
              envvar=PywbemServer.password_envvar,
              help=u'Password for the WBEM server. '
                   u'Default: EnvVar {ev}, or prompted for if --user '
                   u'specified. Use "" to set default in interactive mode.'.
                   format(ev=PywbemServer.password_envvar))
@click.option('--verify/--no-verify', 'verify', default=None,
              # defaulted in code
              envvar=PywbemServer.verify_envvar,
              help=u'If --verify, client verifies the X.509 server '
                   u'certificate presented by the WBEM server during TLS/SSL '
                   u'handshake. If --no-verify client bypasses verification. '
                   u'Default: EnvVar {ev}, or "--verify".'.
                   format(ev=PywbemServer.verify_envvar))
@click.option('--ca-certs', type=str, metavar="CACERTS",
              default=None,  # defaulted in code
              envvar=PywbemServer.ca_certs_envvar,
              help=u'Certificates used to validate the certificate presented '
                   u'by the WBEM server during TLS/SSL handshake: '
                   u'FILE: Use the certs in the specified PEM file; '
                   u'DIR: Use the certs in the PEM files in the specified '
                   u'directory; '
                   u'"certifi" (pywbem 1.0 or later): Use the certs provided '
                   u'by the certifi Python package; '
                   u'Default: EnvVar {ev}, or "certifi" (pywbem 1.0 or later), '
                   u'or the certs in the PEM files in the first existing '
                   u'directory from from a system defined list of directories '
                   u'(pywbem before 1.0).'.
                   format(ev=PywbemServer.ca_certs_envvar))
@click.option('-c', '--certfile', type=str, metavar="FILE",
              # defaulted in code
              envvar=PywbemServer.certfile_envvar,
              help=u'Path name of a PEM file containing a X.509 client '
                   u'certificate that is used to enable TLS/SSL 2-way '
                   u'authentication by presenting the certificate to the '
                   u'WBEM server during TLS/SSL handshake.  Use "" to set '
                   u'default in interactive mode. '
                   u'Default: EnvVar {ev}, or none.'.
                   format(ev=PywbemServer.certfile_envvar))
@click.option('-k', '--keyfile', type=str, metavar='FILE',
              # defaulted in code
              envvar=PywbemServer.keyfile_envvar,
              help=u'Path name of a PEM file containing a X.509 private key '
                   u'that belongs to the certificate in the --certfile file. '
                   u'Not required if the private key is part of the '
                   u'--certfile file. Use "" to set default in interactive '
                   u'mode.'
                   u'Default: EnvVar {ev}, or none.'.
                   format(ev=PywbemServer.keyfile_envvar))
@click.option('-t', '--timeout', type=click.IntRange(0, MAX_TIMEOUT),
              metavar='INT',
              # defaulted in code
              envvar=PywbemServer.timeout_envvar,
              help=u'Client-side timeout in seconds for operations with the '
                   u'WBEM server. '
                   u'Default: EnvVar {ev}, or {default}.'.
                   format(ev=PywbemServer.timeout_envvar,
                          default=DEFAULT_CONNECTION_TIMEOUT))
@click.option('-U', '--use-pull', type=click.Choice(['yes', 'no', 'either']),
              # defaulted in code
              envvar=PywbemServer.use_pull_envvar,
              help=u'Determines whether pull operations are used for '
                   u'operations with the WBEM server that return lists of '
                   u'instances, as follows: '
                   u'"yes" uses pull operations and fails if not supported by '
                   u'the server; '
                   u'"no" uses traditional operations; '
                   u'"either" (default) uses pull operations if supported by '
                   u'the server, and otherwise traditional operations. '
                   u'Default: EnvVar {ev}, or "either".'.
                   format(ev=PywbemServer.use_pull_envvar))
@click.option('--pull-max-cnt', type=int, metavar='INT',
              # defaulted in code
              help=u'Maximum number of instances to be returned by the WBEM '
                   u'server in each open or pull response, if pull operations '
                   u'are used. '
                   u'This is a tuning parameter that does not affect the '
                   u'external behavior of the commands. '
                   u'Default: EnvVar {ev}, or {default}'.
                   format(ev=PywbemServer.pull_max_cnt_envvar,
                          default=DEFAULT_MAXPULLCNT))
@click.option('-T', '--timestats/--no-timestats',
              default=None,
              envvar=PywbemServer.timestats_envvar,
              help=u'Display operation time statistics gathered by pywbemcli '
              u'after each command. Otherwise statistics can be displayed with '
              u'"statistics show" command. '
              u'Default: EnvVar {ev}, or no-timestats.'.
              format(ev=PywbemServer.timestats_envvar))
@click.option('-d', '--default-namespace', type=str, metavar='NAMESPACE',
              default=None,  # default value set in cli function
              envvar=PywbemServer.defaultnamespace_envvar,
              help=u'Default namespace, to be used when commands do not '
                   u'specify the --namespace command option. Use "" to set '
                   u'default in interactive mode. '
                   u'Default: EnvVar {ev}, or {default}.'.
                   format(ev=PywbemServer.defaultnamespace_envvar,
                          default=DEFAULT_NAMESPACE))
@click.option('-o', '--output-format', metavar='FORMAT',
              default=None,  # There is no default value
              help=u'Output format for the command result. '
                   u'The default and allowed output formats are command '
                   u'specific. '
                   u'The default output_format is None so that each command '
                   u'selects its own default format. Use "" to set default '
                   u'in interactive mode. '
                   u'FORMAT is: table formats: [{tb}]; CIM object '
                   u'formats: [{ob}]]; TEXT formats: [{tx}].'.
                   format(tb='|'.join(OUTPUT_FORMAT_GROUPS['TABLE'][0]),
                          ob='|'.join(OUTPUT_FORMAT_GROUPS['CIM'][0]),
                          tx='|'.join(OUTPUT_FORMAT_GROUPS['TEXT'][0])))
@click.option('-l', '--log', type=str, metavar='COMP[=DEST[:DETAIL]],...',
              default=None,  # There is no default value
              envvar=PywbemServer.log_envvar,
              help=u'Enable logging of the WBEM operations, defined by a list '
                   u'of log configuration strings with: '
                   u'COMP: [{comp_choices}]; '
                   u'DEST: [{dest_choices}], default: {dest_default}; '
                   u'DETAIL: [{detail_choices}], default: {detail_default}. '
                   u' Use "" to set default in interactive mode'
                   u'Default: EnvVar {ev}, or {default}.'.
                   format(comp_choices='|'.join(LOGGER_SIMPLE_NAMES),
                          dest_choices='|'.join(LOG_DESTINATIONS),
                          dest_default=DEFAULT_LOG_DESTINATION,
                          detail_choices='|'.join(LOG_DETAIL_LEVELS),
                          detail_default=DEFAULT_LOG_DETAIL_LEVEL,
                          ev=PywbemServer.log_envvar,
                          default='all'))
@click.option('-v', '--verbose/--no-verbose',
              default=None,  # None separates no option from --no-verbose
              help=u'Display extra information about the processing.')
@click.option('--warn/--no-warn', is_flag=True,
              default=None,  # None separates no option from --no-warning
              help=u'Warnings control: True enables display of all Python '
              u'warnings; False leaves warning control to the PYHONWARNINGS '
              u'env var, which by default displays no warnings. '
              u'Default: False.')
@click.option('-C', '--connections-file', metavar='FILE PATH',
              default=None,  # default value set in cli function
              envvar=PywbemServer.connections_file_envvar,
              # Keep help text in sync with connections file definitions in
              # _connection_repository.py:
              help=u'Path name of the connections file to be used. '
                   u'Default: EnvVar {ev}, or "{cf}" in the user\'s home '
                   u'directory (as determined using Python\'s '
                   u'os.path.expanduser("~"). See there for details, '
                   u'particularly for Windows). Use "" to set default '
                   u'in interactive mode. '.
                   format(cf=CONNECTIONS_FILENAME,
                          ev=PywbemServer.connections_file_envvar))
@click.option('--pdb', is_flag=True,
              # defaulted in code
              envvar=PywbemServer.pdb_envvar,
              help=u'Pause execution in the built-in pdb debugger just before '
                   u'executing the command within pywbemcli. Ignored in '
                   u'interactive mode, but can be specified on each '
                   u'interactive command. '
                   u'Default: EnvVar {ev}, or false.'.
                   format(ev=PywbemServer.pdb_envvar))
@click.version_option(
    message='%(prog)s, version %(version)s\npywbem, version {}'.format(
        pywbem_version),
    help=u'Show the version of this command and the pywbem package.')
@add_options(help_option)
@click.pass_context
def cli(ctx, server, connection_name, default_namespace, user, password,
        timeout, verify, certfile, keyfile, ca_certs, output_format, use_pull,
        pull_max_cnt, mock_server, verbose=None, connections_file=None,
        timestats=None, log=None, pdb=None, warn=None):
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

    resolved_mock_server = []

    # Options not allowed when -name is used and when
    # in interactive mode. This disallows modifying values
    # of servers in interactive mode.
    conditional_options = ((default_namespace, 'default_namespace'),
                           (timeout, 'timeout'),
                           (verify, 'verify'),
                           (user, 'user'),
                           (certfile, 'certfile'),
                           (keyfile, 'keyfile'),
                           (ca_certs, 'ca_certs'),
                           (server, 'server'),
                           # Special because we resolve the mock-server list
                           # during initialization.
                           (resolved_mock_server, 'mock-server'))

    # Process cli options to validate options and produce resolved options,
    # i.e. the options with any defaults applied for non None options.
    # Produces new variables resolved... so that later tests can confirm that
    # original variables were None or not None

    if warn:
        warnings.simplefilter('once')
    # else: Leave warning control to the PYTHONWARNINGS env var.

    pywbem_server = None
    resolved_default_namespace = default_namespace or DEFAULT_NAMESPACE
    # Resolved accounts for True, False, None
    resolved_verify = DEFAULT_VERIFY if verify is None else verify

    # There is no default ca_certs
    resolved_ca_certs = ca_certs  # None should be passed on

    if keyfile and not certfile:
        raise click.ClickException(
            'The --keyfile option "{}" is allowed only if the --certfile '
            'option is also used'.format(keyfile))

    # If this env variable is set, execute the file defined by variable.
    # This is private and to be used to preload test scripts for pywbemcli
    # testing.
    if os.getenv(PYWBEMCLI_STARTUP_ENVVAR) and ctx.obj is None:
        _execute_startup_script(os.getenv('PYWBEMCLI_STARTUP_SCRIPT'), verbose)

    # Process mock_server option
    if mock_server:
        resolved_mock_server = _resolve_mock_server(mock_server)
    else:
        resolved_mock_server = None

    # Validate that only one of server, mock_server, and connection name exists
    # We this manually because click does not have way to do mutual exclusion
    # on options.
    _validate_no_server_option_conficts(server, connection_name,
                                        resolved_mock_server)

    resolved_use_pull = USE_PULL_CHOICE[use_pull] if use_pull \
        else USE_PULL_CHOICE[DEFAULT_PULL_CHOICE]

    resolved_pull_max_cnt = pull_max_cnt or DEFAULT_MAXPULLCNT

    resolved_timeout = timeout or DEFAULT_CONNECTION_TIMEOUT

    # Set flag that will be used to indicate server change in
    # in interactive mode so the server can be disconnected after
    # use.
    close_interactive_server = False

    # Command mode (ctx is None) or initial input in interactive mode.
    # Apply the documented option defaults to create a pywbem_server instance
    # and a ContextObj instance
    if ctx.obj is None:  # No context. This is cmd line mode or initial input
        # in interactive mode.
        # Create the PywbemServer object (contains all of the info
        # for the connection defined by the cmd line input)

        connections_repo = ConnectionRepository(
            connections_file or DEFAULT_CONNECTIONS_FILE, verbose)

        pywbem_server = _create_server_instance(server, connection_name,
                                                resolved_default_namespace,
                                                user, password,
                                                resolved_timeout,
                                                resolved_use_pull,
                                                resolved_pull_max_cnt,
                                                resolved_verify,
                                                certfile, keyfile,
                                                resolved_ca_certs,
                                                resolved_mock_server,
                                                connections_repo,
                                                conditional_options,
                                                verbose)

    # Interactive mode cmd line processing (ctx not None)
    # In interactive mode, general options specified in cmd line are used
    # to modify the pywbem_server object and the general options
    # for a single command execution.
    # This requires being able to determine for each option whether it has been
    # specified and is why general options don't define defaults in the
    # decorators that define them.

    else:  # ctx.obj exists. Processing an interactive command.
        # Issue # 920Imposed this limit to avoid confusion of changing
        # connections file in interactive mode
        if connections_file:
            raise click.ClickException('General option "--connections-file" '
                                       'not allowed in interactive mode.')
        connections_repo = ctx.obj.connections_repo
        # Apply the general options from the command line options
        # or from the context object to modify the PywbemServer object and
        # for a new ContextObj for the command
        modified_server = False

        # If --name option, get pywbem_server object from connection
        if connection_name:
            _validate_connections_file(connections_repo)
            pywbem_server = _validate_connection_name(connections_repo,
                                                      connection_name)
            modified_server = True
            close_interactive_server = True

        # If other parameters, modify the existing connection and reset it.
        else:
            if pywbem_server is None:
                # Copy to keep the original clean from any changes.
                # This allows modifications to be made for a single
                # interactive command but not kept beyond the life of
                # that command.
                if ctx.obj.pywbem_server_exists():
                    pywbem_server = deepcopy(ctx.obj.pywbem_server)

        # Modify the currently defined pywbem_server if it is defined
        # with any general options including resetting options and if
        # there are any modifications to pywbem_server, set that modified
        # server into the current context object.
        # In cases where input parameter of "" is allowed to
        # reset option values, the option is tested for "is not None"
        # to include empty string in test.

        if pywbem_server:
            if server:
                if pywbem_server.mock_server:
                    pywbem_server.mock_server = []
                pywbem_server.server = server
                modified_server = True
                close_interactive_server = True
            if mock_server:
                if pywbem_server.server:
                    pywbem_server.server = None
                pywbem_server.mock_server = resolved_mock_server
                modified_server = True
            if user is not None:
                pywbem_server.user = _set_default_if_empty_str(user)
                modified_server = True
            if password is not None:
                pywbem_server.password = _set_default_if_empty_str(password)
                modified_server = True
            if verify is not None:
                pywbem_server.verify = resolved_verify
                modified_server = True
            if ca_certs:
                pywbem_server.ca_certs = ca_certs
                modified_server = True
            if certfile is not None:
                pywbem_server.certfile = _set_default_if_empty_str(certfile)
                modified_server = True
            if keyfile is not None:
                pywbem_server.keyfile = _set_default_if_empty_str(keyfile)
                modified_server = True
            if timeout:
                pywbem_server.timeout = resolved_timeout
                modified_server = True
            if use_pull:
                pywbem_server.use_pull = resolved_use_pull
                modified_server = True
            if default_namespace is not None:
                pywbem_server.default_namespace = \
                    _set_default_if_empty_str(default_namespace,
                                              DEFAULT_NAMESPACE)
                modified_server = True

            # If modified, disconnect existing connection
            # This MUST BE two if statements to work.
            if modified_server:
                if pywbem_server.connected:
                    pywbem_server.disconnect()
            else:
                pywbem_server = ctx.obj.pywbem_server

        else:
            pywbem_server = None

        # The following variables are maintained only in the context_obj and
        # not attached to any particular connection. If the cli argument is
        # None, this argument was not defined as part of this interactive
        # command and the value is set from the existing ctx.obj.

        # These variables are retrieved from the ctx.obj if the parameter
        # value is none (not defined for current interactive command). Note
        # that some of them allow the value "" to be used to reset the
        # general option to its default value.
        #
        if output_format is None:
            output_format = ctx.obj.output_format
        elif output_format == "":
            output_format = None

        if use_pull is None:
            resolved_use_pull = ctx.obj.use_pull

        if pull_max_cnt is None:
            resolved_pull_max_cnt = ctx.obj.pull_max_cnt

        if timestats is None:
            timestats = ctx.obj.timestats

        if log is None:
            log = ctx.obj.log
        elif log == "":
            log = None

        if verbose is None:
            verbose = ctx.obj.verbose

        # Commented out because we do not allow modification of the
        # connection file and have already set connections_repo in line
        # above. This code would have allowed resetting to default.
        # See issue #920
        # if connections_repo is None:
        #    connections_repo = ctx.obj.connections_repo
        # elif connections_repo == "":
        #    connections_repo = DEFAULT_CONNECTIONS_FILE

        if pdb is None:
            pdb = ctx.obj.pdb
        if warn is None:
            warn = ctx.obj.warn

    # Conditionally set the flag to enable warnings
    if warn:
        warnings.simplefilter('once')

    # Create a command context for each command: An interactive command has
    # its own command context as a child of the command context for the
    # command line.
    # Set pull_max_cnt to either resolved or default here so we keep default
    # in persistent file but set working value in context.

    interactive_mode = ctx.obj.interactive_mode if ctx.obj else False
    ctx.obj = ContextObj(pywbem_server, output_format,
                         resolved_use_pull,
                         resolved_pull_max_cnt,
                         timestats,
                         log, verbose, pdb,
                         warn,
                         connections_repo,
                         interactive_mode,
                         close_interactive_server)

    # Env.var PYWBEMCLI_DIAGNOSTICS turns on diagnostic prints for developer
    # use and is therefore not documented.
    if os.getenv('PYWBEMCLI_DIAGNOSTICS'):
        display_click_context(ctx, msg="DIAGNOSTICS-NEWCTX: Initial context:",
                              display_attrs=True)

    _python_nm = sys.version_info[0:2]
    if _python_nm in ((2, 7), (3, 4)):
        pywbemcliwarn(
            "Pywbemcli support for Python {}.{} is deprecated and will be "
            "removed in a future version".
            format(_python_nm[0], _python_nm[1]),
            DeprecationWarning)

    # If no invoked_subcommand, there is no command to execute this flag
    # causes us to start interactive mode
    if ctx.invoked_subcommand is None:
        ctx.obj.interactive_mode = True
        ctx.invoke(repl)

        # Exit interactive mode and exit Pywbemcli. Disconnect any connected
        # server.
        if ctx.obj.is_connected():
            ctx.obj.pywbem_server.disconnect()


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
  <CTRL-r>  <search string>   To search the  command history file.
                              Can be used with <UP>, <DOWN>
                              to display commands that match the search string.
                              Editing the search string updates the search.
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

    In the repl mode, <CTRL-r> man be used to initiate an interactive
    search of the history file.

    Interactive mode also includes an autosuggest feature that makes
    suggestions from the command history as the command the user types in the
    command and options.
    """

    history_file = PYWBEMCLI_HISTORY_FILE
    if history_file.startswith('~'):
        history_file = os.path.expanduser(history_file)

    click.echo("Enter 'help' for help, <CTRL-D> or ':q' "
               "to exit pywbemcli or <CTRL-r> to search history, ")

    prompt_kwargs = {
        'message': PYWBEMCLI_PROMPT,
        'history': FileHistory(history_file),
    }

    if USE_AUTOSUGGEST:
        prompt_kwargs['auto_suggest'] = AutoSuggestFromHistory()

    click_repl.repl(ctx, prompt_kwargs=prompt_kwargs)
