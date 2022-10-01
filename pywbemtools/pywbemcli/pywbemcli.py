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
import warnings
import click
import click_repl
from prompt_toolkit.history import FileHistory
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory

from pywbem import LOGGER_SIMPLE_NAMES, \
    LOG_DESTINATIONS, DEFAULT_LOG_DESTINATION, LOG_DETAIL_LEVELS, \
    DEFAULT_LOG_DETAIL_LEVEL
from pywbem import __version__ as pywbem_version

from pywbem._cim_operations import HTTP_READ_RETRIES

from .config import PYWBEMCLI_NAME_ENVVAR, PYWBEMCLI_SERVER_ENVVAR, \
    PYWBEMCLI_MOCK_SERVER_ENVVAR, \
    PYWBEMCLI_DEFAULT_NAMESPACE_ENVVAR, PYWBEMCLI_USER_ENVVAR, \
    PYWBEMCLI_PASSWORD_ENVVAR, PYWBEMCLI_VERIFY_ENVVAR, \
    PYWBEMCLI_CERTFILE_ENVVAR, PYWBEMCLI_KEYFILE_ENVVAR, \
    PYWBEMCLI_CA_CERTS_ENVVAR, PYWBEMCLI_TIMEOUT_ENVVAR, \
    PYWBEMCLI_USE_PULL_ENVVAR, PYWBEMCLI_CONNECTIONS_FILE_ENVVAR, \
    PYWBEMCLI_PULL_MAX_CNT_ENVVAR, PYWBEMCLI_TIMESTATS_ENVVAR, \
    PYWBEMCLI_LOG_ENVVAR, PYWBEMCLI_PDB_ENVVAR
from ._context_obj import ContextObj, display_click_context
from ._pywbem_server import PywbemServer
from .config import DEFAULT_NAMESPACE, PYWBEMCLI_PROMPT, \
    PYWBEMCLI_HISTORY_FILE, DEFAULT_MAXPULLCNT, DEFAULT_CONNECTION_TIMEOUT, \
    MAX_TIMEOUT, USE_AUTOSUGGEST
from ._connection_repository import ConnectionRepository, \
    ConnectionsFileError
from .._click_extensions import PywbemtoolsTopGroup, GENERAL_OPTS_TXT, \
    SUBCMD_HELP_TXT, MutuallyExclusiveOption
from .._utils import pywbemtools_warn, get_terminal_width, \
    CONNECTIONS_FILENAME, DEFAULT_CONNECTIONS_FILE
from .._options import add_options, help_option
from .._output_formatting import OUTPUT_FORMAT_GROUPS


__all__ = ['cli']

PYWBEMCLI_STARTUP_ENVVAR = "PYWBEMCLI_STARTUP_SCRIPT"

DEFAULT_DEFINITION_NAME = "not-saved"

# Defaults for some options
DEFAULT_VERIFY = True  # The default is to verify
DEFAULT_PULL_CHOICE = 'either'
USE_PULL_CHOICE = {'either': None, 'yes': True, 'no': False, 'default': None}

# Save for general opiton log parameter from the interactive
# command before the current command in some cases.
PREV_LOG_OPTION = None

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


def _get_default_connection(connections_repo, verbose):
    """
    Attempt to get the default connection name from the connections repo
    if there is a repo defined. if there is no repo or no default connection
    name in the repo, returns None.

    Returns:
        String containing valid connection name that is the default connection
        or None if there is no connections repo or no default connection
        defined in the repo

    Raises:
        click.ClickException if the default name exists but the corresponding
        connection definition does not exist.
    """
    try:
        if connections_repo.file_exists():
            connection_name = connections_repo.default_connection_name

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
                    'name cleared.'.
                    format(connection_name,
                           connections_repo.connections_file))
            if verbose:
                click.echo('Current connection: "{}"'
                           .format(connection_name))
            return connection_name

        # returns no if there is no file
        return None

    # Account for other exception from file access
    except ConnectionsFileError as cfc:
        click.echo("{}, {}". format(cfc.__class__.__name__, cfc),
                   err=True)
        raise click.Abort()


def _validate_server_only_options(pywbem_server, user, password, timeout,
                                  verify, certfile, keyfile, ca_certs):
    """
    Validate that the options defined as parameters for this function
    are not set if the server defined is a mock server since these
    parameters are not used in the mock server.  opt_names below define
    the general option names that do not apply to a mock server.
    """
    if pywbem_server.mock_server:
        opts = [user, password, timeout, verify is not None, certfile,
                keyfile, ca_certs]
        if any(opts):
            opt_names = ["--user", "--password", "--timeout",
                         "--verify", "--certfile", "--keyfile",
                         "--ca_certs"]
            errors = [opt_names[c] for c, i in enumerate(opts) if i]
            raise click.ClickException(
                "General option(s): ({0}) not allowed when using a mock "
                "server. This can happen when defining a mock server with "
                "general options '--name', or ""'--mock-server'".
                format(", ".join(errors)))


def _create_server_instance(
        server, connection_name, resolved_default_namespace, user, password,
        resolved_timeout, resolved_use_pull, resolved_pull_max_cnt,
        resolved_verify, certfile, keyfile, ca_certs, resolved_mock_server,
        connections_repo, verbose, default_namespace, use_pull, pull_max_cnt,
        timeout, verify):
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

    Timeout and verify are passed because once resolved there is no way to
    determine if they were provided as general options
    """

    if server or resolved_mock_server:
        connection_name = 'not-saved'
        pywbem_server = PywbemServer(
            server, resolved_default_namespace, name=connection_name,
            user=user, password=password, timeout=resolved_timeout,
            use_pull=resolved_use_pull, pull_max_cnt=resolved_pull_max_cnt,
            verify=resolved_verify, certfile=certfile, keyfile=keyfile,
            ca_certs=ca_certs, mock_server=resolved_mock_server)

        return pywbem_server

    # Server / mock_server were not specified
    # If name cmd line option, get get name from the connections
    # repo or use default name if it exists.
    if connection_name:
        _validate_connections_file(connections_repo, abort=True)
        _validate_connection_name(connections_repo, connection_name)

    # No connection name specified, try default connection name from
    # connections file
    else:
        # If the connections repo exists, try to get the default conneciton
        # definition. Only fail if there is a default but there is no
        # corresponding definition
        connection_name = _get_default_connection(connections_repo, verbose)
        if connection_name is None:
            return None

    pywbem_server = connections_repo[connection_name]

    # At this point pywbem_server was created from either --name or
    # default name which loaded definition from connection file

    # Modify connection properties with other general options that were on
    # command line if it was created from --name or the default
    # server definition in the connections file. All PywbemServer parameters
    # except name can be modified.
    if default_namespace:
        pywbem_server.default_namespace = resolved_default_namespace
    if user:
        pywbem_server.user = user
    if password:
        pywbem_server.password = password
    if timeout:
        pywbem_server.timeout = resolved_timeout
    if use_pull:
        pywbem_server.use_pull = resolved_use_pull
    if pull_max_cnt:
        pywbem_server.pull_max_cnt = resolved_pull_max_cnt
    if verify is not None:
        pywbem_server.verify = resolved_verify
    if certfile:
        pywbem_server.certfile = certfile
    if keyfile:
        pywbem_server.keyfile = keyfile
    if ca_certs:
        pywbem_server.ca_certs = ca_certs

    return pywbem_server


############################################################################
#
#   cli command (main entry point) and definition of all of the pywbemcli
#   general options.
#
############################################################################


# pylint: disable=bad-continuation
# PywbemtoolsTopGroup sets order commands listed in help output
@click.group(invoke_without_command=True, cls=PywbemtoolsTopGroup,
             move_to_end=('connection', 'help', 'repl'),
             context_settings=CONTEXT_SETTINGS,
             options_metavar=GENERAL_OPTS_TXT,
             subcommand_metavar=SUBCMD_HELP_TXT)
@click.option('-n', '--name', 'connection_name', type=str, metavar='NAME',
              cls=MutuallyExclusiveOption,
              mutually_exclusive=["server", 'mock-server'],
              show_mutually_exclusive=False,
              # defaulted in code
              envvar=PYWBEMCLI_NAME_ENVVAR,
              help=u'Use the WBEM server defined by the WBEM connection '
                   u'definition NAME. '
                   u'This option is mutually exclusive with the --server and '
                   u'--mock-server options, since each defines a WBEM server. '
                   u'Default: EnvVar {ev}, or none.'.
                   format(ev=PYWBEMCLI_NAME_ENVVAR))
@click.option('-m', '--mock-server', type=str, multiple=True, metavar="FILE",
              # defaulted in code
              cls=MutuallyExclusiveOption,
              mutually_exclusive=["server", 'name'],
              show_mutually_exclusive=False,
              envvar=PYWBEMCLI_MOCK_SERVER_ENVVAR,
              help=u'Use a mock WBEM server that is automatically created in '
                   u'pywbemcli and populated with CIM objects that are defined '
                   u'in the specified MOF file or Python script file. The '
                   u'files may be specified with relative or absolute path.'
                   u'See the pywbemcli documentation for more information. '
                   u'This option may be specified multiple times, and is '
                   u'mutually exclusive with the --server and --name options, '
                   u'since each defines a WBEM server. '
                   u'Default: EnvVar {ev}, or none.'.
                   format(ev=PYWBEMCLI_MOCK_SERVER_ENVVAR))
@click.option('-s', '--server', type=str, metavar='URL',
              # defaulted in code
              cls=MutuallyExclusiveOption,
              mutually_exclusive=["mock-server", 'name'],
              show_mutually_exclusive=False,
              envvar=PYWBEMCLI_SERVER_ENVVAR,
              help=u'Use the WBEM server at the specified URL with format: '
                   u'[SCHEME://]HOST[:PORT]. '
                   u'SCHEME must be "https" (default) or "http". '
                   u'HOST is a short or long hostname or literal IPV4/v6 '
                   u'address. '
                   u'PORT defaults to 5989 for https and 5988 for http. '
                   u'This option is mutually exclusive with the --mock-server '
                   u'and --name options, since each defines a WBEM server. '
                   u'Default: EnvVar {ev}, or none.'.
                   format(ev=PYWBEMCLI_SERVER_ENVVAR))
@click.option('-u', '--user', type=str, metavar='TEXT',

              default=None,  # There is no default value
              envvar=PYWBEMCLI_USER_ENVVAR,
              help=u'User name for the WBEM server.  Use "" to set default in '
                   u'interactive mode.'
                   u'Default: EnvVar {ev}, or none.'.
                   format(ev=PYWBEMCLI_USER_ENVVAR))
@click.option('-p', '--password', type=str, metavar='TEXT',
              default=None,  # There is not default value
              envvar=PYWBEMCLI_PASSWORD_ENVVAR,
              help=u'Password for the WBEM server. '
                   u'Default: EnvVar {ev}, or prompted for if --user '
                   u'specified. Use "" to set default in interactive mode.'.
                   format(ev=PYWBEMCLI_PASSWORD_ENVVAR))
@click.option('--verify/--no-verify', 'verify', default=None,
              # defaulted in code
              envvar=PYWBEMCLI_VERIFY_ENVVAR,
              help=u'If --verify, client verifies the X.509 server '
                   u'certificate presented by the WBEM server during TLS/SSL '
                   u'handshake. If --no-verify client bypasses verification. '
                   u'Default: EnvVar {ev}, or "--verify".'.
                   format(ev=PYWBEMCLI_VERIFY_ENVVAR))
@click.option('--ca-certs', type=str, metavar="CACERTS",
              default=None,  # defaulted in code
              envvar=PYWBEMCLI_CA_CERTS_ENVVAR,
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
                   format(ev=PYWBEMCLI_CA_CERTS_ENVVAR))
@click.option('-c', '--certfile', type=str, metavar="FILE",
              # defaulted in code
              envvar=PYWBEMCLI_CERTFILE_ENVVAR,
              help=u'Path name of a PEM file containing a X.509 client '
                   u'certificate that is used to enable TLS/SSL 2-way '
                   u'authentication by presenting the certificate to the '
                   u'WBEM server during TLS/SSL handshake.  Use "" to set '
                   u'default in interactive mode. '
                   u'Default: EnvVar {ev}, or none.'.
                   format(ev=PYWBEMCLI_CERTFILE_ENVVAR))
@click.option('-k', '--keyfile', type=str, metavar='FILE',
              # defaulted in code
              envvar=PYWBEMCLI_KEYFILE_ENVVAR,
              help=u'Path name of a PEM file containing a X.509 private key '
                   u'that belongs to the certificate in the --certfile file. '
                   u'Not required if the private key is part of the '
                   u'--certfile file. Use "" to set default in interactive '
                   u'mode.'
                   u'Default: EnvVar {ev}, or none.'.
                   format(ev=PYWBEMCLI_KEYFILE_ENVVAR))
@click.option('-t', '--timeout', type=click.IntRange(0, MAX_TIMEOUT),
              metavar='INT',
              # defaulted in code
              envvar=PYWBEMCLI_TIMEOUT_ENVVAR,
              help=u'Client-side timeout (seconds) on data read for '
                   u'operations with the WBEM server. This integer is the '
                   u'timeout for a single server request. Pywbem retries '
                   u'reads {rt} times so the delay for read timeout failure '
                   u'may be multiple times the timeout value.'
                   u'Default: EnvVar {ev}, or {default}. Min/max: '.
                   format(rt=HTTP_READ_RETRIES, ev=PYWBEMCLI_TIMEOUT_ENVVAR,
                          default=DEFAULT_CONNECTION_TIMEOUT))
@click.option('-U', '--use-pull', type=click.Choice(['yes', 'no', 'either']),
              # defaulted in code
              envvar=PYWBEMCLI_USE_PULL_ENVVAR,
              help=u'Determines whether pull operations are used for '
                   u'operations with the WBEM server that return lists of '
                   u'instances, as follows: '
                   u'"yes" uses pull operations and fails if not supported by '
                   u'the server; '
                   u'"no" uses traditional operations; '
                   u'"either" (default) uses pull operations if supported by '
                   u'the server, and otherwise traditional operations. '
                   u'Default: EnvVar {ev}, or "either".'.
                   format(ev=PYWBEMCLI_USE_PULL_ENVVAR))
@click.option('--pull-max-cnt', type=int, metavar='INT',
              # defaulted in code
              help=u'Maximum number of instances to be returned by the WBEM '
                   u'server in each open or pull response, if pull operations '
                   u'are used. '
                   u'This is a tuning parameter that does not affect the '
                   u'external behavior of the commands. '
                   u'Default: EnvVar {ev}, or {default}'.
                   format(ev=PYWBEMCLI_PULL_MAX_CNT_ENVVAR,
                          default=DEFAULT_MAXPULLCNT))
@click.option('-T', '--timestats/--no-timestats',
              default=None,
              envvar=PYWBEMCLI_TIMESTATS_ENVVAR,
              help=u'Display operation time statistics gathered by pywbemcli '
              u'after each command. Otherwise statistics can be displayed with '
              u'"statistics show" command. '
              u'Default: EnvVar {ev}, or no-timestats.'.
              format(ev=PYWBEMCLI_TIMESTATS_ENVVAR))
@click.option('-d', '--default-namespace', type=str, metavar='NAMESPACE',
              default=None,  # default value set in cli function
              envvar=PYWBEMCLI_DEFAULT_NAMESPACE_ENVVAR,
              help=u'Default namespace, to be used when commands do not '
                   u'specify the --namespace command option. Use "" to set '
                   u'default in interactive mode. '
                   u'Default: EnvVar {ev}, or {default}.'.
                   format(ev=PYWBEMCLI_DEFAULT_NAMESPACE_ENVVAR,
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
              default=None,
              envvar=PYWBEMCLI_LOG_ENVVAR,
              help=u'Enable logging of WBEM operations, defined by a list '
                   u'of log configuration strings with: '
                   u'COMP: [{comp_choices}]; '
                   u'DEST: [{dest_choices}], default: {dest_default}; '
                   u'DETAIL: [{detail_choices}], default: {detail_default}. '
                   u'"all=off" disables all logging. "all" is max logging. '
                   u'EnvVar: {ev}. Default: no logging'.
                   format(comp_choices='|'.join(LOGGER_SIMPLE_NAMES),
                          dest_choices='|'.join(LOG_DESTINATIONS),
                          dest_default=DEFAULT_LOG_DESTINATION,
                          detail_choices='|'.join(LOG_DETAIL_LEVELS),
                          detail_default=DEFAULT_LOG_DETAIL_LEVEL,
                          ev=PYWBEMCLI_LOG_ENVVAR))
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
              envvar=PYWBEMCLI_CONNECTIONS_FILE_ENVVAR,
              # Keep help text in sync with connections file definitions in
              # _connection_repository.py:
              help=u'Path name of the connections file to be used. '
                   u'Default: EnvVar {ev}, or "{cf}" in the user\'s home '
                   u'directory (as determined using Python\'s '
                   u'os.path.expanduser("~"). See there for details, '
                   u'particularly for Windows). Use "" to set default '
                   u'in interactive mode. '.
                   format(cf=CONNECTIONS_FILENAME,
                          ev=PYWBEMCLI_CONNECTIONS_FILE_ENVVAR))
@click.option('--pdb', is_flag=True,
              # defaulted in code
              envvar=PYWBEMCLI_PDB_ENVVAR,
              help=u'Pause execution in the built-in pdb debugger just before '
                   u'executing the command within pywbemcli. Ignored in '
                   u'interactive mode, but can be specified on each '
                   u'interactive command. '
                   u'Default: EnvVar {ev}, or false.'.
                   format(ev=PYWBEMCLI_PDB_ENVVAR))
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
    PYWBEMTOOLS_TERMWIDTH environment variable.

    For more detailed documentation, see:

        https://pywbemtools.readthedocs.io/en/stable/
    """

    # Process cli options to validate options and produce resolved options,
    # i.e. the options with any defaults applied for non None options.
    # Produces new variables resolved... so that later tests can confirm that
    # original variables were None or not None
    if warn:
        warnings.simplefilter('once')
    # else: Leave warning control to the PYTHONWARNINGS env var.

    pywbem_server = None
    resolved_default_namespace = default_namespace or DEFAULT_NAMESPACE
    # Resolved is True, False. Input is True, False, None
    resolved_verify = DEFAULT_VERIFY if verify is None else verify

    if keyfile and not certfile:
        raise click.ClickException(
            'The --keyfile option "{}" is allowed only if the --certfile '
            'option is also used'.format(keyfile))

    # If this env variable is set, execute the file defined by variable.
    # This is private and to be used to preload test scripts for pywbemcli
    # testing, ex. mock of pywbemcli services.
    if os.getenv(PYWBEMCLI_STARTUP_ENVVAR) and ctx.obj is None:
        _execute_startup_script(os.getenv('PYWBEMCLI_STARTUP_SCRIPT'), verbose)

    # Process mock_server option
    resolved_mock_server = _resolve_mock_server(mock_server) if mock_server \
        else None

    resolved_use_pull = USE_PULL_CHOICE[use_pull] if use_pull \
        else USE_PULL_CHOICE[DEFAULT_PULL_CHOICE]

    if pull_max_cnt is not None:
        if pull_max_cnt < 1:
            raise click.ClickException(
                'The --pull_max_cnt option value must be gt 1: "{}" received.'.
                format(pull_max_cnt))
    resolved_pull_max_cnt = pull_max_cnt or DEFAULT_MAXPULLCNT

    resolved_timeout = timeout or DEFAULT_CONNECTION_TIMEOUT

    # Set flag that will be used to indicate server change in
    # in interactive mode so the server can be disconnected after
    # the interactive command that modified the server.
    close_interactive_server = False

    # Command mode (ctx is None) or initial input in interactive mode.
    # Apply the documented option defaults to create a pywbem_server instance
    # and a ContextObj instance
    if ctx.obj is None:  # No context; cmd line or initial interactive input

        connections_repo = ConnectionRepository(
            connections_file or DEFAULT_CONNECTIONS_FILE, verbose)

        # Create PywbemServer instance. the last 3 parameters are needed
        # to determine if the options were input on cmd line since the
        # resolved versions are ambiguous.
        pywbem_server = _create_server_instance(
            server, connection_name, resolved_default_namespace,
            user, password, resolved_timeout, resolved_use_pull,
            resolved_pull_max_cnt, resolved_verify, certfile, keyfile,
            ca_certs, resolved_mock_server, connections_repo, verbose,
            # used in function to test if option exists on cmd line
            default_namespace, use_pull, pull_max_cnt, timeout, verify)

        # Validate no WbemConnection only options used with FakedWBEMConnection
        if pywbem_server:
            _validate_server_only_options(pywbem_server, user, password,
                                          timeout, verify, certfile, keyfile,
                                          ca_certs)

    # Interactive mode cmd line processing (ctx not None)
    # In interactive mode, general options specified in cmd line are used
    # to modify the pywbem_server object and the general options
    # for a single command execution.
    # This requires being able to determine for each option whether it has been
    # specified and is why general options don't define defaults in the
    # decorators that define them.
    # ctx is the higher level context that forms the basis for this
    # command.  the ctx.obj defines parameters that were input with either
    # env variables or the command line pywbemcli startup

    else:  # ctx.obj exists. Processing an interactive command.
        # If connection file general option exists, get the new connection_repo.
        # This overrides the existing ctx defined repo only for current command.
        if connections_file:
            connections_repo = ConnectionRepository(connections_file, verbose)
        elif connections_file == "":
            connections_repo = DEFAULT_CONNECTIONS_FILE
        else:
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
                # PywbemServer has its own copy method that does a
                # recursive copy because the conn objects also have their
                # own copy methods
                if ctx.obj.pywbem_server_exists():
                    pywbem_server = ctx.obj.pywbem_server.copy()

        # Modify the currently defined pywbem_server if it is defined
        # with any general options including resetting options and if
        # there are any modifications to pywbem_server, set that modified
        # server into the current context object and reset it.
        # In cases where input parameter of "" is allowed to
        # reset option values, the option is tested for "is not None"
        # to include empty string in test.

        # In interactive mode, --serve and --mock_server may modify a
        # server definition. On the command line no.

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
                close_interactive_server = True
            if default_namespace is not None:
                pywbem_server.default_namespace = \
                    _set_default_if_empty_str(default_namespace,
                                              DEFAULT_NAMESPACE)
                modified_server = True
                close_interactive_server = True
            if user is not None:
                pywbem_server.user = _set_default_if_empty_str(user)
                modified_server = True
                close_interactive_server = True
            if password is not None:
                pywbem_server.password = _set_default_if_empty_str(password)
                modified_server = True
                close_interactive_server = True
            if verify is not None:
                pywbem_server.verify = resolved_verify
                modified_server = True
                close_interactive_server = True
            if timeout:
                pywbem_server.timeout = resolved_timeout
                modified_server = True
            if use_pull:
                pywbem_server.use_pull = resolved_use_pull
                modified_server = True
            if pull_max_cnt:
                pywbem_server.pull_max_cnt = resolved_pull_max_cnt
                modified_server = True
            if ca_certs:
                pywbem_server.ca_certs = ca_certs
                modified_server = True
                close_interactive_server = True
            if certfile is not None:
                pywbem_server.certfile = _set_default_if_empty_str(certfile)
                modified_server = True
                close_interactive_server = True
            if keyfile is not None:
                pywbem_server.keyfile = _set_default_if_empty_str(keyfile)
                modified_server = True
                close_interactive_server = True

            # If modified, disconnect the just fixed connection. This will
            # cause the modified connection to be initialized. Otherwise
            # use original PywbemServer object from context
            if modified_server:
                if pywbem_server.connected:
                    pywbem_server.disconnect()
            else:
                pywbem_server = ctx.obj.pywbem_server

        else:
            pywbem_server = None

        # Validate that if mock_server, only options specific to mock_server
        # were on the command line
        if pywbem_server:
            _validate_server_only_options(pywbem_server, user, password,
                                          timeout, verify, certfile, keyfile,
                                          ca_certs)

        # The following variables are maintained only in the context_obj and
        # not attached to any particular connection. If the value of each option
        # is its default (None, or in some cases "") the value  is set to the
        # the original cmd line input value (ctx.obj.xxx). Otherwise it is set
        # to the value presented with the general options part of this
        # interactive command.

        # The "" test for some formats allows the user to specifically set the
        # value to the default
        if output_format is None:
            output_format = ctx.obj.output_format
        elif output_format == "":
            output_format = None

        if timestats is None:
            timestats = ctx.obj.timestats

        if verbose is None:
            verbose = ctx.obj.verbose

        # Logging requires using configure_log() each time the log changes and
        # the change depends on the command_line log option value and the
        # value of the log option for previous log command.  This code only
        # modifies the log configuration if pywbem_server exists and is
        # already connected. Otherwise PywbemServer.connect defines the
        # log configuration
        cmd_line_log = ctx.obj.log
        global PREV_LOG_OPTION  # pylint: disable=global-statement
        new_log_configuration = None
        if log is None:
            # If cmd_line log value exists reset to that value
            if cmd_line_log:
                log = cmd_line_log
                new_log_configuration = cmd_line_log

            else:  # no cmd_line log so turn logging off
                if PREV_LOG_OPTION:
                    new_log_configuration = "all=off"
            PREV_LOG_OPTION = ""

        else:  # general_option --log exists. Set new if not the same
            if PREV_LOG_OPTION and log != PREV_LOG_OPTION:
                new_log_configuration = log
            elif log != cmd_line_log:
                new_log_configuration = log
            PREV_LOG_OPTION = log

        if new_log_configuration:
            if pywbem_server and pywbem_server.connected:
                pywbem_server.set_logger_config(new_log_configuration)

        if verbose:
            click.echo("Log configured to {}".format(log))

        # NOTE: connection-file general option handled as first test because
        # it could be used for other option processing

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
    if _python_nm in ((2, 7),):
        pywbemtools_warn(
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
