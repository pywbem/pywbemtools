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

NOTE: Commands are ordered in help display by their order in this file.
"""

from __future__ import absolute_import, print_function

from copy import deepcopy
import click
import six

from pywbem import Error

from .pywbemcli import cli
from ._common import CMD_OPTS_TXT, GENERAL_OPTS_TXT, \
    SUBCMD_HELP_TXT, pick_one_from_list, format_table, \
    raise_pywbem_error_exception, validate_output_format, fold_strings
from ._common_options import add_options, help_option
from ._pywbem_server import PywbemServer
from ._connection_repository import ConnectionRepository
from ._context_obj import ContextObj
from ._click_extensions import PywbemcliGroup, PywbemcliCommand


@cli.group('connection', cls=PywbemcliGroup, options_metavar=GENERAL_OPTS_TXT,
           subcommand_metavar=SUBCMD_HELP_TXT)
@add_options(help_option)
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


@connection_group.command('export', cls=PywbemcliCommand,
                          options_metavar=CMD_OPTS_TXT)
@add_options(help_option)
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


@connection_group.command('show', cls=PywbemcliCommand,
                          options_metavar=CMD_OPTS_TXT)
@click.argument('name', type=str, metavar='NAME', required=False)
@click.option('--show-password', is_flag=True,
              default=False,
              help='If set, show existing password in results. Otherwise, '
                   'password is masked')
@add_options(help_option)
@click.pass_obj
def connection_show(context, name, **options):
    """
    Show a WBEM connection definition or the current connection.

    Show the name and attributes of a WBEM connection definition or the
    current connection, as follows:

    * If the NAME argument is specified, the connection definition with that
      name from the connections file is shown.

    * If the NAME argument is '?', the command presents a list of connection
      definitions from the connections file and prompts the user for
      selecting one, which is then shown.

    * If the NAME argument is omitted, the current connection is shown.

    Example showing a named connection definition:

    \b
      pywbemcli connection show svr1
        name: svr1
        ...

    Example for prompting for a connection definition:

    \b
      pywbemcli connection show ?
        0: svr1
        1: svr2
      Input integer between 0 and 2 or Ctrl-C to exit selection: : 0
        name: svr1
          ...
    """
    context.execute_cmd(lambda: cmd_connection_show(context, name, options))


@connection_group.command('delete', cls=PywbemcliCommand,
                          options_metavar=CMD_OPTS_TXT)
@click.argument('name', type=str, metavar='NAME', required=False)
@add_options(help_option)
@click.pass_obj
def connection_delete(context, name):
    """
    Delete a WBEM connection definition.

    Delete a named connection definition from the connections file. If the NAME
    argument is omitted, prompt for selecting one of the connection definitions
    in the connections file.

    Example:

      pywbemcli connection delete blah
    """
    context.execute_cmd(lambda: cmd_connection_delete(context, name))


@connection_group.command('select', cls=PywbemcliCommand,
                          options_metavar=CMD_OPTS_TXT)
@click.argument('name', type=str, metavar='NAME', required=False)
@click.option('-d', '--default', is_flag=True,
              default=False,
              help='If set, the connection is set to be the default connection '
                   ' in the connections file in addition to setting it as the '
                   'current connection.')
@add_options(help_option)
@click.pass_obj
def connection_select(context, name, **options):
    """
    Select a WBEM connection definition as current or default.

    Select the connection definition named NAME from the connections file to
    be the current connection. The connection definition in the connections
    file must exist. If the NAME argument is omitted, a list of connection
    definitions from the connections file is presented with a prompt for the
    user to select a connection definition.

    If the --default option is set, the default connection is set to the
    selected connection definition, in addition.
    Once defined, the default connection will be used as a default in future
    executions of pywbemcli if none of the server-defining general options
    (i.e. --server, --mock-server, or --name) was used.

    The 'connection list' command marks the current connection with '*' and
    the default connection with '#'.

    Example of selecting a default connection in command mode:

    \b
      pywbemcli connection select myconn --default
      pywbemcli connection show
      name: myconn
        . . .

    Example of selecting just the current connection in interactive mode:

    \b
      pywbemcli
      pywbemcli> connection select myconn
      pywbemcli> connection show
      name: myconn
        . . .
    """

    context.execute_cmd(lambda: cmd_connection_select(context, name, options))


@connection_group.command('test', cls=PywbemcliCommand,
                          options_metavar=CMD_OPTS_TXT)
@add_options(help_option)
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


@connection_group.command('save', cls=PywbemcliCommand,
                          options_metavar=CMD_OPTS_TXT)
@click.argument('name', type=str, metavar='NAME', required=True)
@add_options(help_option)
@click.pass_obj
def connection_save(context, name):
    """
    Save the current connection to a new WBEM connection definition.

    Save the current connection to the connections file as a connection
    definition named NAME. The NAME argument is required.
    If a connection definition with that name already exists, it is
    overwritten without warning.

    In the interactive mode, general options that are connection related
    are applied to the current connection before it is saved.

    Examples:

      pywbemcli --server https://srv1 connection save mysrv
    """
    context.execute_cmd(lambda: cmd_connection_save(context, name))


@connection_group.command('list', cls=PywbemcliCommand,
                          options_metavar=CMD_OPTS_TXT)
@click.option('-f', '--full', is_flag=True,
              default=False,
              help='If set, display the full table. Otherwise display '
                   'a brief view(name, server, mock_server columns).')
@add_options(help_option)
@click.pass_obj
def connection_list(context, **options):
    """
    List the WBEM connection definitions.

    This command displays all entries in the connections file and the
    current connection if it exists and is not in the connections file as
    a table.

    \b
    '#' before the name indicates the default connection.
    '*' before the name indicates that it is the current connection.

    See also the 'connection select' command.
    """
    context.execute_cmd(lambda: cmd_connection_list(context, options))


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
    click.echo('export {}={}'.format(name, value))


def if_export_statement(name, value):
    """Export the statement if the value is not None"""
    if value is not None:
        export_statement(name, value)


def is_default_connection(connection):
    """
    Returns True if connection is the default connection. Where
    default connection is defined in repository.
    """

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
                                show_state=False, show_password=False):
    """
    Common function to display the connection information.  Note that this
    could also have been part of the context object since this is just the
    info from that object.
    """

    output_format = validate_output_format(context.output_format, 'TABLE')

    # Build state string, mock_server obj, password
    state_str = ''
    if show_state:
        state = []
        if is_current_connection(connection, context):
            state.append("current")
        if is_default_connection(connection):
            state.append("default")
        if state:
            state_str = ' ({})'.format(", ".join(state))

    if connection.password:
        disp_password = connection.password if show_password else '******'
    else:
        disp_password = connection.password

    headers = ["name", 'value  (state)']

    if connection.mock_server:
        mock_server = fold_strings(connection.mock_server, 20,
                                   fold_list_items=True,
                                   break_long_words=False,
                                   break_on_hyphens=False)
    else:
        mock_server = None

    if connection.ca_certs:
        ca_certs = fold_strings(connection.ca_certs, 20,
                                fold_list_items=True,
                                break_long_words=False)
    else:
        ca_certs = None

    rows = [['name', "{}{}".format(connection.name, state_str)],
            ['server', connection.server],
            ['default-namespace', connection.default_namespace],
            ['user', connection.user],
            ['password', disp_password],
            ['timeout', connection.timeout],
            ['use-pull', connection.use_pull],
            ['verify', connection.verify],
            ['certfile', connection.certfile],
            ['keyfile', connection.keyfile],
            ['mock-server', mock_server],
            ['ca-certs', ca_certs]]

    context.spinner_stop()

    click.echo(format_table(rows, headers, title='Connection status:',
                            table_format=output_format))


def get_current_connection_name(context):
    """
    Return the name of the current connection or None if there is no
    current connection
    """
    return context.pywbem_server.name if context.pywbem_server else None


def raise_repository_empty(connections):
    """
    Raise exception with message that repo is empty.
    """
    raise click.ClickException(
        'Connection repository {} empty'.format(connections.connections_file))


def select_connection(name, context, connections):
    """
    Use the interactive mode to select the connection from the list of
    connections in the connections file. If the name is provided, it is tested
    against the names in the connections file.  If it is not provided,
    """
    context.spinner_stop()

    if not connections:
        raise_repository_empty(connections)

    if name:
        if name in connections:
            return name
        raise click.ClickException(
            'Connection name "{}" does not exist in connections file: {}'
            .format(name, connections.connections_file))

    conn_names = sorted(list(six.iterkeys(connections)))
    return pick_one_from_list(context, conn_names,
                              "Select a connection or Ctrl-C to abort.")


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
    context.spinner_stop()
    svr = context.pywbem_server
    if not svr:
        raise click.ClickException("No server currently defined as current")

    export_statement(PywbemServer.server_envvar, svr.server)

    if_export_statement(PywbemServer.defaultnamespace_envvar,
                        svr.default_namespace)
    if_export_statement(PywbemServer.user_envvar, svr.user)
    if_export_statement(PywbemServer.password_envvar, svr.password)
    if_export_statement(PywbemServer.verify_envvar, svr.verify)
    if_export_statement(PywbemServer.certfile_envvar, svr.certfile)
    if_export_statement(PywbemServer.keyfile_envvar, svr.keyfile)
    if_export_statement(PywbemServer.ca_certs_envvar, svr.ca_certs)
    if_export_statement(PywbemServer.timeout_envvar, svr.timeout)
    if_export_statement(PywbemServer.use_pull_envvar, svr.use_pull)


def cmd_connection_show(context, name, options):
    """
    Show the parameters that make up the current connection information if
    name is None. If Name exists, shows connections in connections file.
    """

    connections = ConnectionRepository()

    cname = get_current_connection_name(context)
    # If no name arg, fallback to selection unless there is no connections file
    if not name:
        name = cname or '?'
        if not cname and not connections:
            raise click.ClickException('No current connection and no '
                                       'connections file {}.'
                                       .format(connections.connections_file))

    # ? means to ask for connections file. However fallback to current
    # if there is no connections file and fail if no current.
    if name == '?':
        # No connections exit in connections file.
        if not connections:
            if context.pywbem_server:
                show_connection_information(
                    context,
                    context.pywbem_server,
                    show_state=True,
                    show_password=options['show_password'])
                return

        name = select_connection(None, context, connections)

    # Have a name. If there are connections and this name is in connections
    # and that name is not current, use it. If current name is same as
    # name, use the current version.
    if connections:
        # If name in connections same as currrent connection. use current
        connection = connections[name] if name in connections and \
            cname != name else context.pywbem_server
    else:   # nothing in connections file
        if cname != name:
            raise click.ClickException('Name "{}" not current and no '
                                       'connections file {}'
                                       .format(name,
                                               connections.connections_file))
        connection = context.pywbem_server

    if connection is None:
        raise click.ClickException("No connection definition exists.")

    show_connection_information(context,
                                connection,
                                show_state=True,
                                show_password=options['show_password'])


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
        context.spinner_stop()
        click.echo('Connection successful')
    except Error as er:
        raise_pywbem_error_exception(er)


def cmd_connection_select(context, name, options):
    """
    Select an existing connection to use as the current WBEM server. This
    command accepts the click_context since it updates that context.

    If the --default flag is set, also set this connection as the persistent
    default conneciton.
    """
    connections = ConnectionRepository()

    name = select_connection(name, context, connections)

    new_ctx = ContextObj(connections[name],
                         context.output_format,
                         context.use_pull,
                         context.pull_max_cnt,
                         context.timestats,
                         context.log,
                         context.verbose,
                         context.pdb)

    # Update the root context making this context the basis for future
    # commands in the current interactive session
    ContextObj.update_root_click_context(new_ctx)
    context.spinner_stop()
    if options['default']:
        connections.set_default_connection(name)
        click.echo('"{}" default and current'.format(name))
    else:
        click.echo('"{}" current'.format(name))


def cmd_connection_delete(context, name):
    """
    Delete a connection definition from the set of connections defined.

    This may be either defined by the optional name parameter or if there
    is no name provided, a select list will be presented for the user
    to select the connection to be deleted.
    """
    connections = ConnectionRepository()

    # Select the connection with prompt if name is None.
    # This also stops the spinner
    name = select_connection(name, context, connections)

    cname = get_current_connection_name(context)
    connections.delete(name)

    default = 'default ' if cname and cname == name else ''
    click.echo('Deleted {} connection "{}".'.format(default, name))


def cmd_connection_save(context, name):
    """
    Saves the connection named name or the current connection of no name
    """

    current_connection = context.pywbem_server
    if not current_connection:
        raise click.ClickException('No current connection connection. Use '
                                   '"connection list" to see more connection '
                                   'information')
    save_connection = deepcopy(current_connection)
    save_connection.name = name

    connections = ConnectionRepository()

    context.spinner_stop()

    connections.add(save_connection.name, save_connection)


def cmd_connection_list(context, options):
    """
    Dump all of the current servers in the persistent repository line
    by line.  This method displays the information as a table independent
    of the value of the cmd line output_format general option.
    """
    def build_row(options, name, svr):
        """
        Append one row to the list
        """
        if options['full']:
            return [name, svr.server, svr.default_namespace, svr.user,
                    svr.timeout, svr.use_pull, svr.verify, svr.certfile,
                    svr.keyfile, "\n".join(svr.mock_server)]
        return [name, svr.server, "\n".join(svr.mock_server)]

    connections = ConnectionRepository()
    output_format = validate_output_format(context.output_format, 'TABLE')

    # build the table structure
    rows = []
    cur_sym = '*'  # single char representing current connection
    dflt_sym = '#'  # single char representing persisted default connection
    for name, svr in connections.items():
        cc = cur_sym if is_current_connection(svr, context) else ''
        dc = dflt_sym if is_default_connection(svr) else ''
        name = '{}{}{}'.format(cc, dc, name)

        rows.append(build_row(options, name, svr))

    # add current connection if not in persistent connections
    current_connection = context.pywbem_server or None

    if current_connection:
        cname = current_connection.name
        if cname not in connections:
            cname = '{}{}'.format('*', cname)
            svr = current_connection
            rows.append(build_row(options, cname, svr))

    # NOTE: Does not show ca_certs because that creates a very big table
    # in particular if you use the default.
    if options['full']:
        headers = ['name', 'server', 'namespace', 'user',
                   'timeout', 'use_pull', 'verify', 'certfile', 'keyfile',
                   'mock-server']
    else:
        headers = ['name', 'server', 'mock-server']

    context.spinner_stop()
    table_type = 'full' if options['full'] else 'brief'
    click.echo(format_table(
        sorted(rows),
        headers,
        title='WBEM server connections({}): ({}: default, {}: current)'.format(
            table_type, dflt_sym, cur_sym),
        table_format=output_format))
