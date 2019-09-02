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
    Show the current connection or a WBEM connection definition.

    Display the parameters of the current connection, or if the optional NAME
    argument is specified, of the named WBEM connection definition from the
    connections file.

    Examples:

      pywbemcli --name server1 connection show

      pywbemcli connection show server1
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
@click.pass_obj
def connection_select(context, name):
    """
    Select a WBEM connection definition as the current connection.

    Make a named connection definition from the connections file the current
    connection. If the NAME argument is omitted, prompt for selecting one of
    the connection definitions in the connections file.

    This command is useful in the interactive mode of pywbemcli.

    The selection of the current connection is not saved across interactive
    sessions of pywbemcli.

    Examples:

      pywbemcli

      > connection select myconn

      > connection select          # prompts
    """

    context.execute_cmd(lambda: cmd_connection_select(context, name))


@connection_group.command('add', options_metavar=CMD_OPTS_TXT)
@click.option('-n', '--name', type=str, metavar='NAME',
              required=True,
              help='Name for the new WBEM connection definition.')
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
def connection_add(context, **options):
    """
    Add a new WBEM connection definition from specified options.

    Create a new WBEM connection definition in the connections file from
    the specified options. A connection definition with that name must not
    yet exist.

    The current connection remains unchanged by this command.

    Examples:

      pywbemcli --name newsrv connection add --server https://srv1
    """
    context.execute_cmd(lambda: cmd_connection_add(context, options))


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
@click.option('-n', '--name', type=str, metavar="NAME",
              default=None,
              help='Name for the new WBEM connection definition.')
@add_options(verify_option)
@click.pass_obj
def connection_save(context, **options):
    """
    Save the current connection as a new WBEM connection definition.

    Create a new WBEM connection definition in the connections file from
    the current connection. A connection definition with that name must not
    yet exist.

    This command is useful when you have defined a connection on the command
    line and want to save it in the connections file for later use.

    Examples:

      pywbemcli --server https://srv1 connection save --name mysrv
    """
    context.execute_cmd(lambda: cmd_connection_save(context, options))


@connection_group.command('list', options_metavar=CMD_OPTS_TXT)
@click.pass_obj
def connection_list(context):
    """
    List the WBEM connection definitions.

    List the WBEM connection definitions in the connections file as a table.

    In the table, the current connection is marked with an "*" after its name.

    Examples:

      pywbemcli connection list
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
                  svr.server, sep,
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
        new_server = PywbemServer(
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
        current_svr._name = options['name']  # pylint: disable=protected-access
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
        row = [name, svr.server, svr.default_namespace, svr.user,
               svr.timeout, svr.no_verify, svr.certfile,
               svr.keyfile, svr.log, "\n".join(svr.mock_server)]
        rows.append(row)

    headers = ['name', 'server', 'namespace', 'user',
               'timeout', 'no-verify', 'certfile', 'keyfile', 'log',
               'mock-server']

    headers, rows = hide_empty_columns(headers, rows)

    context.spinner.stop()
    click.echo(format_table(sorted(rows), headers,
                            title='WBEM server connections:',
                            table_format=context.output_format))
