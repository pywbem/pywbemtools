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
disk which is kept in sync with changes made with the add/delete commands.
"""
from __future__ import absolute_import

from copy import deepcopy
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
    Command group for WBEM connection definitions.

    This command group defines commands to manage persistent WBEM connection
    definitions that have a name. The connection definitions are stored in a
    connections file named 'pywbemcli_connection_definitions.yaml' in the
    current directory. The connection definition name can be used as a
    shorthand for the WBEM server via the '--name' general option.

    In addition to the command-specific options shown in this help text, the
    general options (see 'pywbemcli --help') can also be specified before the
    'connection' keyword.
    """
    pass  # pylint: disable=unnecessary-pass


@connection_group.command('export', options_metavar=CMD_OPTS_TXT)
@click.pass_obj
def connection_export(context):
    """
    Export the current connection.

    Display commands that set pywbemcli environment variables to the parameters
    of the current connection.

    Examples:

      pywbemcli --name srv1 connection export

      pywbemcli --server https://srv1 --user me --password pw connection export
    """
    context.execute_cmd(lambda: cmd_connection_export(context))


@connection_group.command('show', options_metavar=CMD_OPTS_TXT)
@click.argument('name', type=str, metavar='NAME', required=False)
@click.pass_obj
def connection_show(context, name):
    """
    Show connection info of a WBEM connection definition.

    This command displays the WBEM connection definition of a single
    connection as follows:

    * NAME argument exists; show that WBEM connections file.

    * NAME argument does not exist; show existing current connection or
      presents list for selection

    * Name argument is '?'; presents list of connections for selection

    This command displays all the variables that make up current
    WBEM connection.

    \b
      pywbemcli connection show svr1
        name: svr1
        ...
      pywbemcli connection show ?
        0: svr1
        1: svr2
    Input integer between 0 and 2 or Ctrl-C to exit selection: : 0
      name: svr1
      ...
    """
    context.execute_cmd(lambda: cmd_connection_show(context, name))


@connection_group.command('delete', options_metavar=CMD_OPTS_TXT)
@click.argument('name', type=str, metavar='NAME', required=False)
@add_options(verify_option)
@click.pass_obj
def connection_delete(context, name, **options):
    """
    Delete a WBEM connection definition.

    Delete a named connection definition from the connections file. If the NAME
    argument is omitted, prompt for selecting one of the connection definitions
    in the connections file.

    Example:

      pywbemcli connection delete blah
    """
    context.execute_cmd(lambda: cmd_connection_delete(context, name, options))


@connection_group.command('select', options_metavar=CMD_OPTS_TXT)
@click.argument('name', type=str, metavar='NAME', required=False)
@click.option('-d', '--default', is_flag=True,
              default=False,
              help='If set, the connection is set to be the default connection '
                   ' in the connections file in addition to setting it as the '
                   'current connection.')
@click.pass_obj
def connection_select(context, name, **options):
    """
    Select a WBEM connection definition as current or default.

    Selects a connection from the persistently stored named connections if NAME
    exists in the store to be the current connection. If the NAME argument does
    not exist, a list of connections from the connections definition file is
    presented with a prompt for the user to select a connection.

    Default and current connction are set if the --default option exists;
    otherwise only the connection in the current interactive session is set .
    Once define the default connection will be used as the server definition in
    future execution of pywbemcli if there is no server definition (--server or
    --name or --mock-server) general option.

    Connection list shows all connections and if any are default or current.

    \b
    Example of selecting a connection and setting the default:
      $ pywbemcli
      pywbemcli> connection select myconn --default
      pywbemcli> :quit
      $ pywbemcli show
      name: myconn
        server: http://localhost
    """

    context.execute_cmd(lambda: cmd_connection_select(context, name, options))


@connection_group.command('add', options_metavar=CMD_OPTS_TXT)
@click.argument('name', type=str, metavar='NAME', required=True)
@click.option('--input-name', type=str, metavar='CONNECTION-NAME',
              required=False,
              help='If this option exists, it is the name of an existing '
                   'persistent definition that will be added to the '
                   'connections file with the NAME argument.  All other '
                   'options will be ignored.')
@click.option('-m', '--mock-server', type=str, multiple=True, metavar="FILE",
              default=None,
              help='Use a mock WBEM server that is automatically created in '
                   'pywbemcli and populated with CIM objects that are defined '
                   'in the specified MOF file or Python script file. '
                   'See the pywbemcli documentation for more information. '
                   'This option may be specified multiple times, and is '
                   'mutually exclusive with the --server option, '
                   'since each defines a WBEM server. '
                   'Default: None.')
@click.option('-s', '--server', type=str, metavar='URL',
              default=None,
              help='Use the WBEM server at the specified URL with format: '
                   '[SCHEME://]HOST[:PORT]. '
                   'SCHEME must be "https" (default) or "http". '
                   'HOST is a short or long hostname or literal IPV4/v6 '
                   'address. '
                   'PORT defaults to 5989 for https and 5988 for http. '
                   'This option is mutually exclusive with the --mock-server '
                   'option, since each defines a WBEM server. '
                   'Default: None.'.
              format(ev=PywbemServer.server_envvar))
@click.option('-u', '--user', type=str, metavar="TEXT",
              default=None,
              help='User name for the WBEM server. '
                   'Default: None.')
@click.option('-p', '--password', type=str, metavar="TEXT",
              default=None,
              help='Password for the WBEM server. '
                   'Default: Prompted for if --user specified.')
@click.option('-N', '--no-verify', is_flag=True,
              default=False,
              help='If true, client does not verify the X.509 server '
                   'certificate presented by the WBEM server during TLS/SSL '
                   'handshake. '
                   'Default: False.')
@click.option('--ca-certs', type=str, metavar="FILE",
              default=None,
              help='Path name of a file or directory containing certificates '
                   'that will be matched against the server certificate '
                   'presented by the WBEM server during TLS/SSL handshake. '
                   'Default: [{dirs}].'.
              format(dirs=', '.join(DEFAULT_CA_CERT_PATHS)))
@click.option('-c', '--certfile', type=str, metavar="FILE",
              default=None,
              help='Path name of a PEM file containing a X.509 client '
                   'certificate that is used to enable TLS/SSL 2-way '
                   'authentication by presenting the certificate to the '
                   'WBEM server during TLS/SSL handshake. '
                   'Default: None.')
@click.option('-k', '--keyfile', type=str, metavar="FILE",
              default=None,
              help='Path name of a PEM file containing a X.509 private key '
                   'that belongs to the certificate in the --certfile file. '
                   'Not required if the private key is part of the '
                   '--certfile file.'
                   'Default: None.')
@click.option('-t', '--timeout', type=click.IntRange(0, MAX_TIMEOUT),
              metavar='INT',
              default=DEFAULT_CONNECTION_TIMEOUT,
              help='Client-side timeout in seconds for operations with the '
                   'WBEM server. '
                   'Default: {default}.'.
              format(default=DEFAULT_CONNECTION_TIMEOUT))
@click.option('-U', '--use-pull', type=click.Choice(['yes', 'no', 'either']),
              default='either',
              help='Determines whether pull operations are used for '
                   'operations with the WBEM server that return lists of '
                   'instances, as follows: '
                   '"yes" uses pull operations and fails if not supported by '
                   'the server; '
                   '"no" uses traditional operations; '
                   '"either" (default) uses pull operations if supported by '
                   'the server, and otherwise traditional operations. '
                   'Default: "either".')
@click.option('--pull-max-cnt', type=int, metavar='INT',
              default=DEFAULT_MAXPULLCNT,
              help='Maximum number of instances to be returned by the WBEM '
                   'server in each response, if pull operations are used. '
                   'This is a tuning parameter that does not affect the '
                   'external behavior of the commands. '
                   'Default: {default}'.
              format(default=DEFAULT_MAXPULLCNT))
@click.option('-d', '--default-namespace', type=str, metavar='NAMESPACE',
              default=DEFAULT_NAMESPACE,
              help='Default namespace, to be used when commands do not '
                   'specify the --namespace command option. '
                   'Default: {default}.'.
              format(default=DEFAULT_NAMESPACE))
@click.option('-l', '--log', type=str, metavar='COMP[=DEST[:DETAIL]],...',
              default=None,
              help='Enable logging of the WBEM operations, defined by a list '
                   'of log configuration strings with: '
                   'COMP: [{comp_choices}]; '
                   'DEST: [{dest_choices}], default: {dest_default}; '
                   'DETAIL: [{detail_choices}], default: {detail_default}. '
                   'Default: {default}.'.
              format(comp_choices='|'.join(LOGGER_SIMPLE_NAMES),
                     dest_choices='|'.join(LOG_DESTINATIONS),
                     dest_default=DEFAULT_LOG_DESTINATION,
                     detail_choices='|'.join(LOG_DETAIL_LEVELS),
                     detail_default=DEFAULT_LOG_DETAIL_LEVEL,
                     default='all'))
@add_options(verify_option)
@click.pass_obj
def connection_add(context, name, **options):
    """
    Add a new WBEM connection definition from specified options.

    Create a new WBEM connection definition named NAME in the connections file
    from the specified options. A connection definition with that name must not
    yet exist.

    The NAME argument is required. One of --server,  --mock-server, or --name
    option  is required to define the server for the new connection. All other
    properties are optional.

    Adding a connection does not set the new connection as the current
    connection definition. Use the connection select command to set a
    particular connection definition as the current connection.

      pywbemcli connection add newsvr --server https://srv1
    """
    context.execute_cmd(lambda: cmd_connection_add(context, name, options))


@connection_group.command('test', options_metavar=CMD_OPTS_TXT)
@click.pass_obj
def connection_test(context):
    """
    Test the current connection with a predefined WBEM request.

    Execute the EnumerateClassNames operation on the default namespace against
    the current connection to confirm that the connection exists and is
    working.

    Examples:

      pywbemcli --name mysrv connection test
    """
    context.execute_cmd(lambda: cmd_connection_test(context))


@connection_group.command('save', options_metavar=CMD_OPTS_TXT)
@click.argument('name', type=str, metavar='NAME', required=True)
@add_options(verify_option)
@click.pass_obj
def connection_save(context, name, **options):
    """
    Save a connection to a new WBEM connection definition named NAME.

    Create a new WBEM connection definition in the connections file from the
    current connection A connection definition with the name NAME must not yet
    exist. The NAME argument (the name of the new connection) is required.

    Examples:

      pywbemcli --server https://srv1 connection save mysrv
    """
    context.execute_cmd(lambda: cmd_connection_save(context, name, options))


@connection_group.command('list', options_metavar=CMD_OPTS_TXT)
@click.pass_obj
def connection_list(context):
    """
    List the WBEM connection definitions.

    This command displays all entries in the connections file and the
    current connection if it exists and is not in the connections file as
    a table.

    \b
    '#' before the name indicates the default connection.
    '*' before the name indicates that it is the current connection.
    See connection select.
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


def is_default_connection(connection):
    """Returns True if connection is the default connection"""

    default_connection = ConnectionRepository().get_default_connection_name()
    if default_connection and default_connection == connection.name:
        return True
    return False


def is_current_connection(connection, context):
    """Returns True if connection named name is the default connection"""

    current_connection = context.pywbem_server or None
    if current_connection and current_connection.name == connection.name:
        return True
    return False


def show_connection_information(context, connection, separate_line=True,
                                show_state=False):
    """
    Common function to display the connection information.  Note that this
    could also have been part of the context object since this is just the
    info from that object.
    """
    state_str = ''
    if show_state:
        state = []
        if is_current_connection(connection, context):
            state.append("current")
        if is_default_connection(connection):
            state.append("default")
        if state:
            state_str = ' (%s)' % ", ".join(state)

    sep = '\n  ' if separate_line else ', '
    context.spinner.stop()

    click.echo('\nname: %s%s%sserver: %s%sdefault-namespace: %s'
               '%suser: %s%spassword: %s%stimeout: %s%sno-verify: %s%s'
               'certfile: %s%skeyfile: %s%suse-pull: %s%spull-max-cnt: %s%s'
               'mock-server: %s%slog: %s'
               % (connection.name, state_str, sep,
                  connection.server, sep,
                  connection.default_namespace, sep,
                  connection.user, sep,
                  connection.password, sep,
                  connection.timeout, sep,
                  connection.no_verify, sep,
                  connection.certfile, sep,
                  connection.keyfile, sep,
                  connection.use_pull, sep,
                  connection.pull_max_cnt, sep,
                  ", ".join(connection.mock_server), sep,
                  connection.log))


def get_current_connection_name(context):
    """
    Return the name of the current connection or None if there is no
    current connection
    """
    return context.pywbem_server.name if context.pywbem_server else None


def get_connection_name(name, context, connections, include_current=False):
    """
    If a name is provided, test to see if it is a valid connection name.
    If no name is provided, get list of names for and present selection
    list to the user.
    If include_current, the current connection is included in the list to
    select
    """
    # If no name and context exists with name, use it. Otherwise
    #
    cname = get_current_connection_name(context)
    # alternative to include the current connection name in the list
    if not name:
        if include_current:
            name = cname or '?'
        else:
            name = '?'

    if name == "?":
        context.spinner.stop()
        # get all names from dictionary

        conn_names = sorted(list(six.iterkeys(connections)))
        if include_current and cname:
            conn_names.append(cname)
        if conn_names:
            name = pick_one_from_list(context, conn_names,
                                      "Select a connection or Ctrl_C to abort.")
        else:
            raise click.ClickException(
                'Connection repository %s empty' % connections.connections_file)

    if include_current and cname:
        if cname == name:
            return name

    if name not in connections:
        raise click.ClickException(
            'Connection name "%s" does not exist' % name)

    return name

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

    export_statement(PywbemServer.server_envvar, svr.server)

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
    name = get_connection_name(name, context, connections, include_current=True)

    if name in connections:
        connection = connections[name]
    else:
        if context.pywbem_server:
            connection = context.pywbem_server
        else:
            raise click.ClickException("No server set as current.")

    show_connection_information(context, connection, show_state=True)


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


def cmd_connection_select(context, name, options):
    """
    Select an existing connection to use as the current WBEM server. This
    command accepts the click_context since it updates that context.

    If the --default flag is set, also set this connection as the persistent
    default conneciton.
    """
    connections = ConnectionRepository()

    name = get_connection_name(name, context, connections)

    connection = connections[name]
    new_ctx = ContextObj(connections[name],
                         context.output_format,
                         connection.use_pull,
                         connection.pull_max_cnt,
                         context.timestats,
                         context.log,
                         context.verbose)

    # update the root context making this context the basis for future
    # commands in the current interactive session
    ContextObj.update_root_click_context(new_ctx)
    context.spinner.stop()
    if options['default']:
        connections.set_default_connection(name)
        click.echo('"%s" default and current' % name)
    else:
        click.echo('"%s" current' % name)


def cmd_connection_delete(context, name, options):
    """
    Delete a connection definition from the set of connections defined.

    This may be either defined by the optional name parameter or if there
    is no name provided, a select list will be presented for the user
    to select the connection to be deleted.
    """
    connections = ConnectionRepository()

    name = get_connection_name(name, context, connections)

    context.spinner.stop()
    if options['verify']:
        click.echo('Verify delete of %s' % name)
        show_connection_information(context,
                                    connections[name],
                                    separate_line=False)
        if not verify_operation('Execute delete', msg=True):
            return

    cname = get_current_connection_name(context)
    connections.delete(name)

    default = 'default ' if cname and cname == name else ''
    click.echo('Deleted %sconnection "%s".' % (default, name))


# pylint: disable=unused-argument
def cmd_connection_add(context, name, options):
    """
    Create a new connection object from the input arguments and options and
    put it into the PYWBEMCLI_SERVERS dictionary.
    """
    server = options['server']
    mock_server = options['mock_server']
    connections = ConnectionRepository()
    if name in connections:
        raise click.ClickException('Connection name "%s" already defined'
                                   % name)

    if options['input_name']:
        input_name = options['input_name']
        if input_name not in connections:
            raise click.ClickException('Connection "%s" not in repository' %
                                       input_name)
        new_connection = connections[input_name]
        new_connection._name = name  # pylint: disable=protected-access

    else:
        if not mock_server and not server:
            raise click.ClickException('Add failed; missing server definition. '
                                       'A server using either "--server" or '
                                       '"--mock-server" required.')

        if mock_server and server:
            raise click.ClickException('Add failed; "--server" and '
                                       '"--mock-server" are mutuallly '
                                       'exclusive.')
        try:
            new_connection = PywbemServer(
                server=server,
                default_namespace=options['default_namespace'],
                name=name,
                user=options['user'],
                password=options['password'],
                timeout=options['timeout'],
                no_verify=options['no_verify'],
                certfile=options['certfile'],
                keyfile=options['keyfile'],
                ca_certs=options['ca_certs'],
                mock_server=mock_server,
                log=options['log'])

        except ValueError as ve:
            raise click.ClickException('Add failed. %s' % ve)

    context.spinner.stop()
    if options['verify']:
        click.echo('Verify add of %s' % new_connection.name)
        show_connection_information(context, new_connection,
                                    separate_line=False)
        if not verify_operation("Execute add connection", msg=True):
            return

    connections.add(name, new_connection)


def cmd_connection_save(context, name, options):
    """
    Saves the connection named name or the current connection of no name
    """
    current_connection = context.pywbem_server
    if not current_connection:
        raise click.ClickException('No current connection connection. Use '
                                   '"connection list" to see more connection '
                                   'information')
    save_connection = deepcopy(current_connection)
    save_connection._name = name  # pylint: disable=protected-access

    connections = ConnectionRepository()
    if save_connection.name in connections:
        raise click.ClickException('%s is already defined as a server' %
                                   save_connection.name)
    context.spinner.stop()
    if options['verify']:
        click.echo('Verify save of %s' % current_connection.name)
        click.echo(show_connection_information(context, current_connection,
                                               separate_line=False))
        if not verify_operation('Execute save', msg=True):
            return

    connections.add(save_connection.name, save_connection)


def cmd_connection_list(context):
    """
    Dump all of the current servers in the persistent repository line
    by line.  This method displays the information as a table independent
    of the value of the cmd line output_format general option.
    """
    connections = ConnectionRepository()

    # build the table structure
    rows = []
    cur_sym = '*'  # single char representing current connection
    dflt_sym = '#'  # single char representing persisted default connection
    for name, svr in connections.items():
        cc = cur_sym if is_current_connection(svr, context) else ''
        dc = dflt_sym if is_default_connection(svr) else ''
        name = '%s%s%s' % (cc, dc, name)
        row = [name, svr.server, svr.default_namespace, svr.user,
               svr.timeout, svr.no_verify, svr.certfile,
               svr.keyfile, svr.log, "\n".join(svr.mock_server)]
        rows.append(row)

    # add current connection if not in persistent connections
    current_connection = context.pywbem_server or None
    if current_connection:
        cname = current_connection.name
        if cname not in connections:
            cname = '%s%s' % ('*', cname)
            svr = current_connection
            rows.append([cname, svr.server, svr.default_namespace, svr.user,
                         svr.timeout, svr.no_verify, svr.certfile,
                         svr.keyfile, svr.log, "\n".join(svr.mock_server)])

    headers = ['name', 'server', 'namespace', 'user',
               'timeout', 'no-verify', 'certfile', 'keyfile', 'log',
               'mock-server']

    headers, rows = hide_empty_columns(headers, rows)

    context.spinner.stop()
    click.echo(format_table(
        sorted(rows),
        headers,
        title='WBEM server connections: (%s: default, %s: current)' % (dflt_sym,
                                                                       cur_sym),
        table_format=context.output_format))
