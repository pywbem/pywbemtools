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
Click Command definition for the connection command group which includes
cmds to list add, delete, show, and test server definitions in the
connection information.  This also maintains a definition of servers on
disk which is kept in sync with changes made with the add/delete subcommands.
"""
from __future__ import absolute_import

import click
import six
from pywbem import Error, DEFAULT_CA_CERT_PATHS, LOGGER_SIMPLE_NAMES, \
    LOG_DESTINATIONS, DEFAULT_LOG_DESTINATION, LOG_DETAIL_LEVELS, \
    DEFAULT_LOG_DETAIL_LEVEL

from .pywbemcli import cli
from ._common import CMD_OPTS_TXT, pick_one_from_list, format_table, \
    verify_operation, hide_empty_columns
from ._common_options import add_options, verify_option
from ._pywbem_server import PywbemServer
from .config import DEFAULT_NAMESPACE, DEFAULT_CONNECTION_TIMEOUT, \
    DEFAULT_MAXPULLCNT
from ._connection_repository import ConnectionRepository
from .config import MAX_TIMEOUT
from ._context_obj import ContextObj


@cli.group('connection', options_metavar=CMD_OPTS_TXT)
def connection_group():
    """
    Command group for persistent WBEM connections.

    This command group defines commands to manage persistent WBEM connections
    that have a name. The connections are stored in a connections file named
    'pywbemcliservers.json' in the current directory. The connection name can
    be used as a shorthand for the WBEM server via the '--name' general option.

    In addition to the command-specific options shown in this help text, the
    general options (see 'pywbemcli --help') can also be specified before the
    'connection' keyword.
    """
    pass  # pylint: disable=unnecessary-pass


@connection_group.command('export', options_metavar=CMD_OPTS_TXT)
@click.pass_obj
def connection_export(context):
    """
    Export the current connection information.

    Creates an export statement for each connection variable and outputs
    the statement to the conole.

    """
    context.execute_cmd(lambda: cmd_connection_export(context))


@connection_group.command('show', options_metavar=CMD_OPTS_TXT)
@click.argument('name', type=str, metavar='NAME', required=False,)
@click.pass_obj
def connection_show(context, name):
    """
    Show current or NAME connection information.

    This subcommand displays all the variables that make up the current
    WBEM connection if the optional NAME argument is NOT provided. If NAME not
    supplied, a list of connections from the connections definition file
    is presented with a prompt for the user to select a NAME.

    The information on the connection named is displayed if that name is in
    the persistent repository.
    """
    context.execute_cmd(lambda: cmd_connection_show(context, name))


@connection_group.command('delete', options_metavar=CMD_OPTS_TXT)
@click.argument('name', type=str, metavar='NAME', required=False,)
@add_options(verify_option)
@click.pass_obj
def connection_delete(context, name, **options):
    """
    Delete a named WBEM connection.

    Delete connection information from the persistent store
    for the connection defined by NAME. The NAME argument is optional.

    If NAME not supplied, a select list presents the list of connection
    definitions for selection.

    Example:
      connection delete blah
    """
    context.execute_cmd(lambda: cmd_connection_delete(context, name, options))


@connection_group.command('select', options_metavar=CMD_OPTS_TXT)
@click.argument('name', type=str, metavar='NAME', required=False,)
@click.pass_obj
def connection_select(context, name):
    """
    Select a connection from connections file.

    Selects a connection from the persistently stored set of named connections
    if NAME exists in the store. The NAME argument is optional.  If NAME not
    supplied, a list of connections from the connections definition file
    is presented with a prompt for the user to select a NAME.

    Select state is not persistent.

    Examples:

       connection select <name>    # select the defined <name>

       connection select           # presents select list to pick connection
    """

    context.execute_cmd(lambda: cmd_connection_select(context, name))


# pylint: disable=bad-continuation
@connection_group.command('add', options_metavar=CMD_OPTS_TXT)
@click.option('-s', '--server', type=str, metavar='SERVER', required=False,
              help='Required hostname or IP address with scheme of the '
                   'WBEM server in format:\n[{scheme}://]{host}[:{port}]\n'
                   '* Scheme: must be "https" or "http" [Default: "https"]\n'
                   '* Host: defines short/fully qualified DNS hostname, '
                   'literal IPV4 address (dotted), or literal IPV6 address\n'
                   '* Port: (optional) defines WBEM server port to be used '
                   '[Defaults: 5988(HTTP) and 5989(HTTPS)].\n')
@click.option('-n', '--name', type=str, metavar='NAME', required=True,
              help='Required name for the connection(optional, see --server).  '
                   'This is the name for this defined WBEM server in the'
                   ' connections file')
@click.option('-d', '--default-namespace', type=str,
              metavar='NAMESPACE',
              default=DEFAULT_NAMESPACE,
              help="Default namespace to use in the target WBEM server if no "
                   "namespace is defined in the subcommand"
                   " (Default: {of}).".format(of=DEFAULT_NAMESPACE))
@click.option('-u', '--user', type=str,
              help="User name for the WBEM server connection. ")
@click.option('-p', '--password', type=str,
              envvar=PywbemServer.password_envvar,
              help="Password for the WBEM server. Will be requested as part "
                   " of initialization if user name exists and it is not "
                   " provided by this option.")
@click.option('-t', '--timeout', type=click.IntRange(0, MAX_TIMEOUT),
              help="Operation timeout for the WBEM server in seconds. "
                   "Default: " + "%s" % DEFAULT_CONNECTION_TIMEOUT)
@click.option('-N', '--no-verify', is_flag=True,
              help='If set, client does not verify server certificate.')
@click.option('-c', '--certfile', type=str,
              help="Server certfile. Ignored if no-verify flag set. ")
@click.option('-k', '--keyfile', type=str,
              help="Client private key file. ")
@click.option('-U', '--use-pull',
              envvar=PywbemServer.use_pull_envvar,
              type=click.Choice(['yes', 'no', 'either']),
              default='either',
              help='Determines whether pull operations are used for '
                   'EnumerateInstances, AssociatorInstances, '
                   'ReferenceInstances, and ExecQuery operations.\n'
                   '* "yes": pull operations required; if server '
                   'does not support pull, the operation fails.\n'
                   '* "no": forces pywbemcli to use only the '
                   'traditional non-pull operations.\n'
                   '* "either": pywbemcli trys first pull and then '
                   ' traditional operations.')
@click.option('--pull-max-cnt', type=int,
              help='Maximium object count of objects to be returned for '
                   'each request if pull operations are used. Must be  a '
                   'positive non-zero integer.' +
                   '[Default: {}]'.format(DEFAULT_MAXPULLCNT))
@click.option('-l', '--log', type=str, metavar='COMP=DEST:DETAIL,...',
              help='Enable logging of CIM Operations and set a component '
                   'to destination, and detail level\n'
                   '(COMP: [{c}], Default: {cd}) '
                   'DEST: [{d}], Default: {dd}) '
                   'DETAIL:[{dl}], Default: {dll})'
                   .format(c='|'.join(LOGGER_SIMPLE_NAMES),
                           cd='all',
                           d='|'.join(LOG_DESTINATIONS),
                           dd=DEFAULT_LOG_DESTINATION,
                           dl='|'.join(LOG_DETAIL_LEVELS),
                           dll=DEFAULT_LOG_DETAIL_LEVEL))
@click.option('-m', '--mock-server', type=str, multiple=True,
              metavar="FILENAME",
              help='If this option is defined, a mock WBEM server is '
                   'constructed as the target WBEM server and the option value '
                   'defines a MOF or Python file to be used to populate the '
                   'mock repository. This option may be used multiple times '
                   'where each use defines a single file or file_path.'
                   'See the pywbemcli documentation for more information.')
@click.option('--ca_certs', type=str,
              help='File or directory containing certificates that will be '
                   'matched against a certificate received from the WBEM '
                   'server. Set the --no-verify-cert option to bypass '
                   'client verification of the WBEM server certificate. '
                   'Default: Searches for matching certificates in the '
                   'following system directories:'
                   ' ' + ("\n".join("%s" % p for p in DEFAULT_CA_CERT_PATHS)))
@add_options(verify_option)
@click.pass_obj
def connection_add(context, **options):
    """
    Create a new named WBEM connection.

    This subcommand creates and saves a named connection from the
    input options in the connections file.

    The new connection can be referenced by the name argument in
    the future.  This connection object is capable of managing all of the
    properties defined for WBEMConnections.

    The NAME and URI arguments MUST exist. They define the server uri
    and the unique name under which this server connection information
    will be stored. All other properties are optional.

    Adding a connection does not the new connection as the current connection.
    Use `connection select` to set a particular stored connection definition
    as the current connection.

    A new connection can also be defined by supplying the parameters on the
    command line and using the `connection save` command to put it into the
    connection repository.
    """
    context.execute_cmd(lambda: cmd_connection_add(context, options))


@connection_group.command('test', options_metavar=CMD_OPTS_TXT)
@click.pass_obj
def connection_test(context):
    """
    Execute a predefined WBEM request.

    This executes a predefined request against the current WBEM server to
    confirm that the connection exists and is working.

    It executes EnumerateClassNames on the default namespace as the test.
    """
    context.execute_cmd(lambda: cmd_connection_test(context))


@connection_group.command('save', options_metavar=CMD_OPTS_TXT)
@click.option('-n', '--name', type=str,
              metavar="Connection name",
              help='If defined, this changes the name of the connection to '
              'be saved. This allows renaming the current connection '
              'as part of saving it.')
@add_options(verify_option)
@click.pass_obj
def connection_save(context, **options):
    """
    Save current connection to connections file.

    Saves the current connection to the connections file if
    it does not already exist in that file.

    This is useful when you have defined a connection on the command line and
    want to set it into the connections file.
    """
    context.execute_cmd(lambda: cmd_connection_save(context, options))


@connection_group.command('list', options_metavar=CMD_OPTS_TXT)
@click.pass_obj
def connection_list(context):
    """
    List the entries in the connections file.

    This subcommand displays all entries in the connections file as
    a table using the command line output_format to define the
    table format.

    An "*" after the name indicates the currently selected connection.
    """
    context.execute_cmd(lambda: cmd_connection_list(context))


################################################################
#
#   Common methods for The action functions for the connection click group
#
###############################################################


def export_statement(name, value):
    """ Export the name/value provided as:
        export name=value. We do not actually export but output the
        exprot definition.
    """
    if not isinstance(value, six.string_types):
        value = str(value)
    click.echo('export %s=%s' % (name, value))


def if_export_statement(name, value):
    """Export the statement if the value is not None"""
    if value:
        export_statement(name, value)


def show_connection_information(context, svr, separate_line=True):
    """
    Common function to display the connection information.  Note that this
    could also have been part of the context object since this is just the
    info from that object.
    """
    sep = '\n  ' if separate_line else ', '
    context.spinner.stop()

    click.echo('\nname: %s%sserver: %s%sdefault-namespace: %s'
               '%suser: %s%spassword: %s%stimeout: %s%sno-verify: %s%s'
               'certfile: %s%skeyfile: %s%suse-pull: %s%spull-max-cnt: %s%s'
               'mock-server: %s%slog: %s'
               % (svr.name, sep,
                  svr.server_url, sep,
                  svr.default_namespace, sep,
                  svr.user, sep,
                  svr.password, sep,
                  svr.timeout, sep,
                  svr.no_verify, sep,
                  svr.certfile, sep,
                  svr.keyfile, sep,
                  svr.use_pull, sep,
                  svr.pull_max_cnt, sep,
                  ", ".join(svr.mock_server), sep,
                  svr.log))

    if svr.mock_server and context.verbose:
        click.echo(context.conn.display_repository())

################################################################
#
#   Common methods for The action functions for the connection click group
#
###############################################################


def cmd_connection_export(context):
    """
        Save the current connection information to env variables using an
        export statement
    """
    context.spinner.stop()
    svr = context.pywbem_server
    if not svr:
        raise click.ClickException("No server currently defined as current")

    export_statement(PywbemServer.server_envvar, svr.server_url)

    if_export_statement(PywbemServer.defaultnamespace_envvar,
                        svr.default_namespace)
    if_export_statement(PywbemServer.user_envvar, svr.user)
    if_export_statement(PywbemServer.password_envvar, svr.password)
    if_export_statement(PywbemServer.timeout_envvar, svr.timeout)
    if_export_statement(PywbemServer.no_verify_envvar, svr.no_verify)
    if_export_statement(PywbemServer.certfile_envvar, svr.certfile)
    if_export_statement(PywbemServer.keyfile_envvar, svr.keyfile)
    if_export_statement(PywbemServer.ca_certs_envvar, svr.ca_certs)


def cmd_connection_show(context, name):
    """
    Show the parameters that make up the current connection information
    """
    connections = ConnectionRepository()

    if name:
        if name in connections:
            svr = connections[name]
        else:
            raise click.ClickException("Name %s not in servers repository" %
                                       name)
    else:
        if context.pywbem_server:
            svr = context.pywbem_server
        else:
            raise click.ClickException("No server set as current.")

    show_connection_information(context, svr)


def cmd_connection_test(context):
    """
    Test the current connection with a single command on the default_namespace.
    Uses enumerateClassNames against current workspace as most general
    possible operations that should work on all servers that support class
    operation. Even if class operations are not supported, a return from the
    server such as "unsupported" indicates the server exists.
    """
    try:
        context.conn.EnumerateClassNames()
        context.spinner.stop()
        click.echo('Connection successful')
    except Error as er:
        raise click.ClickException("%s: %s" % (er.__class__.__name__, er))


def cmd_connection_select(context, name):
    """
    Select an existing connection to use as the current WBEM server. This
    command accepts the click_context since it updates that context.
    """
    connections = ConnectionRepository()

    if not name:
        # get all names from dictionary
        conn_names = list(six.iterkeys(connections))
        conn_names = sorted(conn_names)
        if conn_names:
            name = pick_one_from_list(context, conn_names,
                                      "Select a connection or Ctrl_C to abort.")
        else:
            raise click.ClickException(
                'Connection repository %s empty' % connections.connections_file)

    if name in connections:
        pywbem_server = connections[name]
        new_ctx = ContextObj(pywbem_server,
                             context.output_format,
                             pywbem_server.use_pull,
                             pywbem_server.pull_max_cnt,
                             context.timestats,
                             context.log,
                             context.verbose)
        ctx = click.get_current_context()
        ctx.obj = new_ctx
        # update all contexts with new ContextObj
        parent_ctx = ctx.parent
        while parent_ctx is not None:
            parent_ctx.obj = ctx.obj
            parent_ctx = parent_ctx.parent
    else:
        raise click.ClickException(
            'Connection name "%s" does not exist' % name)


def cmd_connection_delete(context, name, options):
    """
    Delete a connection definition from the set of connections defined.

    This may be either defined by the optional name parameter or if there
    is no name provided, a select list will be presented for the user
    to select the connection to be deleted.
    """
    connections = ConnectionRepository()

    if not name:
        # get all names from dictionary
        conn_names = list(six.iterkeys(connections))
        conn_names = sorted(conn_names)
        if not conn_names:
            raise click.ClickException(
                'Connection repository %s empty' % connections.connections_file)

        context.spinner.stop()
        name = pick_one_from_list(context, conn_names,
                                  "Select a connection or CTRL_C to abort.")

    # name defined. Test if in servers.
    if name in connections:
        if connections[name] == context.pywbem_server:
            click.echo('Deleting current connection %s' % name)
        context.spinner.stop()
        if options['verify']:
            click.echo(show_connection_information(context,
                                                   connections[name],
                                                   separate_line=False))
            if not verify_operation('Execute delete', msg=True):
                return
        connections.delete(name)
    else:
        raise click.ClickException('%s not a defined connection name' % name)


# pylint: disable=unused-argument
def cmd_connection_add(context, options):
    """
    Create a new connection object from the input arguments and options and
    put it into the PYWBEMCLI_SERVERS dictionary.
    """
    name = options['name']
    server = options['server']
    mock_server = options['mock_server']
    connections = ConnectionRepository()
    if name in connections:
        raise click.ClickException('Connection name "%s" already defined'
                                   % name)

    if not mock_server and not server:
        raise click.ClickException('Add failed; missing server definition. A '
                                   'server using either "--server" or '
                                   '"--mock-server" required.')

    try:
        new_server = PywbemServer(server, options['default_namespace'],
                                  name,
                                  user=options['user'],
                                  password=options['password'],
                                  timeout=options['timeout'],
                                  no_verify=options['no_verify'],
                                  certfile=options['certfile'],
                                  keyfile=options['keyfile'],
                                  ca_certs=options['ca_certs'],
                                  mock_server=options['mock_server'],
                                  log=options['log'])

    except ValueError as ve:
        raise click.ClickException('Add failed. %s' % ve)

    context.spinner.stop()
    if options['verify']:
        click.echo(show_connection_information(context, new_server,
                                               separate_line=False))
        if not verify_operation("Execute add connection", msg=True):
            return

    connections.add(name, new_server)


def cmd_connection_save(context, options):
    """
    Sets the current connection into the persistent connection repository
    """
    current_svr = context.pywbem_server
    connections = ConnectionRepository()
    if options['name']:
        current_svr._name = options['name']
    if current_svr.name in connections:
        raise click.ClickException('%s is already defined as a server' %
                                   current_svr.name)
    context.spinner.stop()
    if options['verify']:
        click.echo(show_connection_information(context, current_svr,
                                               separate_line=False))
        if not verify_operation('Execute save', msg=True):
            return

    connections.add(current_svr.name, current_svr)


def cmd_connection_list(context):
    """
    Dump all of the current servers in the persistent repository line
    by line.  This method displays the information as a table independent
    of the value of the cmd line output_format general option.
    """
    connections = ConnectionRepository()
    if context.pywbem_server:
        current_server_name = context.pywbem_server.name
    else:
        current_server_name = None

    # build the table structure
    rows = []
    for name, svr in connections.items():
        # if there is a current server, and it is this item in list
        # append * to name
        if context.pywbem_server:
            if name == current_server_name:
                name = name + "*"
        row = [name, svr.server_url, svr.default_namespace, svr.user,
               svr.timeout, svr.no_verify, svr.certfile,
               svr.keyfile, svr.log, "\n".join(svr.mock_server)]
        rows.append(row)

    headers = ['name', 'server uri', 'namespace', 'user',
               'timeout', 'no-verify', 'certfile', 'keyfile', 'log',
               'mock_server']

    headers, rows = hide_empty_columns(headers, rows)

    context.spinner.stop()
    click.echo(format_table(sorted(rows), headers,
                            title='WBEM server connections:',
                            table_format=context.output_format))
